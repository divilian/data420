
import numpy as np
import matplotlib.pyplot as plt

delta_t = 1/7                    # weeks (1 day)
t = np.arange(0,52*25,delta_t)   # weeks (25 yrs)

def run_sim(
    earnings_rate_d = .45,    # ($earned/$capital)/week
    earnings_rate_pj = .45,   # ($earned/$capital)/week
    investment_frac_d = .32,  # ($reinvested/$earned)/week
    investment_frac_pj = .32, # ($reinvested/$earned)/week
    depr_rate_d = .1,         # ($depreciated/$capital)/week
    depr_rate_pj = .1,        # ($depreciated/$capital)/week
    economy_cc = 10000,       # $/week (in earnings) saturation point
    plot_axis = None,         # draw plot on this axis (or None)
    plot_title = "",          # subtitle for plot, if any
    main=True
):

    d_capital = np.empty(len(t))      # $
    d_capital[0] = 450
    pj_capital = np.empty(len(t))     # $
    pj_capital[0] = 450

    profits_d = np.empty(len(t))      # $
    profits_d[0] = 0
    profits_pj = np.empty(len(t))     # $
    profits_pj[0] = 0

    total_earnings_d = 0
    total_earnings_pj = 0
    earnings_d = 0
    earnings_pj = 0

    for i in range(1,len(t)):

        #earnings_rate_d += np.random.normal(0, .001, 1)[0]
        #earnings_rate_pj += np.random.normal(0, .001, 1)[0]

        logistic_factor = 1 - (earnings_d + earnings_pj) / economy_cc

        # Flows.
        earnings_d = (d_capital[i-1] * earnings_rate_d * logistic_factor)
        total_earnings_d += earnings_d
        investment_d = earnings_d * investment_frac_d
        profits_d[i] = earnings_d * (1 - investment_frac_d)

        earnings_pj = (pj_capital[i-1] * earnings_rate_pj * logistic_factor)
        total_earnings_pj += earnings_pj
        investment_pj = earnings_pj * investment_frac_pj
        profits_pj[i] = earnings_pj * (1 - investment_frac_pj)

        depr_d = d_capital[i-1] * depr_rate_d
        depr_pj = pj_capital[i-1] * depr_rate_pj

        # Primes.
        d_capital_prime = investment_d - depr_d
        pj_capital_prime = investment_pj - depr_pj

        # Stocks.
        d_capital[i] = (d_capital[i-1] + d_capital_prime * delta_t)
        pj_capital[i] = (pj_capital[i-1] + pj_capital_prime * delta_t)

    if plot_axis:
        years = t/52
        plot_axis.plot(
            years,
            d_capital,
            color="blue",
            linestyle="solid",
            linewidth=2,
            label="Dominos capital" if main else "",
        )
        plot_axis.plot(
            years,
            profits_d,
            color="blue",
            linestyle="dashed",
            linewidth=2,
            label="Dominos profits" if main else "",
        )
        plot_axis.plot(
            years,
            pj_capital,
            color="red",
            linestyle="solid",
            linewidth=1.5,
            label="Papa John's capital" if main else "",
        )
        plot_axis.plot(
            years,
            profits_pj,
            color="red",
            linestyle="dashed",
            linewidth=1.5,
            label="Papa John's profits" if main else "",
        )
        plot_axis.set_title(plot_title)
        plot_axis.set_xlabel("years")
        plot_axis.set_ylabel("$")


fig, axs = plt.subplots(
    nrows=2,
    sharex=True,
    figsize=(13,8),
    constrained_layout=True,
)
run_sim(
    earnings_rate_d = .45,
    earnings_rate_pj = .45,
    plot_axis = axs[0],
    plot_title = "Both companies: weekly earnings rate = .45 on the dollar"
)
run_sim(
    earnings_rate_d = .46,
    earnings_rate_pj = .45,
    plot_axis = axs[1],
    plot_title = "Dominos weekly earnings rate = .46; Papa John's: .45",
    main=False
)

fig.suptitle("Competitive exclusion model")
fig.legend()
fig.savefig("pizza_competition.svg")
