# RDL backtest inputs (committed before the first run)

Rules first, then values. Each value is set by the rule, not by judgement of the outcome. Where the source is dated after the decision date, or unverified, it is flagged. The held-out case (leaded petrol) is not prepared here.

## A. Problem-structure inputs

### Rules
- **n_major_actors**: number of countries that together account for 80% of the harmful activity, in the latest year before the decision date.
- **substitutes**: 0 = none known; 0.25 = known but costlier or worse for nearly all uses; 0.5 = comparable cost for part of the uses; 0.75 = comparable for most uses; 1 = drop-in at similar cost.
- **economic_share**: value of goods and services directly dependent on the activity, as a share of GDP.

### Values

| Input | Ozone 1985-06 | Climate 1997-11 | Climate 2015-11 |
|---|---|---|---|
| n_major_actors | 12 | 20 | 19 |
| substitutes | 0.5 | 0.25 | 0.5 |
| economic_share | 0.005 | 0.10 | 0.10 |

### Sources and flags
- Ozone n = 12: RFF, 1 Feb 1983, "a dozen countries account for 80 percent of CFC production". Dated before the decision. Note: this counts production; the climate counts are emissions. Cross-check from data/owid_ozone_depleting_substance_consumption.csv: 6 countries for 80% of CFC + halon consumption in 1986 (dated after the decision; first year in the file).
- Climate n = 20 (1996) and 19 (2014): computed from data/owid_annual_co2_emissions.csv, countries only.
- Ozone substitutes = 0.5: RFF 1983, "All substitutes require compromise of some performance characteristics"; aerosol propellant uses had already been replaced in the US after its 1978 aerosol ban (not separately sourced here: **unverified**). Christian Science Monitor, 9 Aug 1989: substitutes "two to five times more expensive" (**dated after the decision**).
- Climate 1997 substitutes = 0.25: no dated source attached yet (**unverified**); the rule is applied on the common description of renewables in 1997 as costlier for nearly all uses.
- Climate 2015 substitutes = 0.5: Lazard LCOE v9.0, reported by RenewEconomy on 18 Nov 2015: best-case unsubsidised wind $32/MWh and utility solar $58/MWh, cheaper than gas and coal. This covers electricity only, which is part of the uses. Dated inside the decision month, before Paris (30 Nov 2015).
- Ozone economic_share = 0.005: CFC production and use generated "$28 billion worth of goods and services" in the US in 1988 (encyclopedia.com, citing unnamed source; **dated after the decision**), against US GDP of about $5.2 trillion (not separately sourced).
- Climate economic_share = 0.10: Enerdata (2011), world energy spending about 10% of world GDP using 1990 and 2010 data (**source dated after 1997**; the 1990 figure was knowable).

## B. Pipeline-bottleneck profiles

### Rules (each score in 0 to 1; higher = stronger, except contradiction)
- **validation**: 0.25 hypothesis only; 0.5 assessed by an international scientific body, no observed effect attributed; 0.75 observed effect attributed with stated uncertainty; 1 assessed as extremely likely or settled.
- **translation**: 0 nothing; 0.25 framework convention without targets; 0.5 non-binding targets, or binding targets covering a minority of the activity; 0.75 binding targets covering most of it; 1 binding targets on all major actors.
- **budget**: 0 none; 0.25 research funding only; 0.5 a dedicated international fund; 0.75 a fund sized to the problem.
- **deployment**: change in the harmful activity over the five years before the decision: rising >10% = 0; rising 0-10% = 0.25; falling <10% = 0.5; falling 10-50% = 0.75; falling >50% = 1.
- **persistence**: no rule found that separates these cases at their decision dates; set to 0.5 for all (flagged).
- **contradiction**: 0.75 if public subsidies to the harmful activity were documented at the decision date; 0.25 otherwise.

### Values

| Score | Ozone 1985-06 | Climate 1997-11 | Climate 2015-11 |
|---|---|---|---|
| validation | 0.5 | 0.75 | 1.0 |
| translation | 0.25 | 0.5 | 0.5 |
| budget | 0.25 | 0.5 | 0.5 |
| deployment | 0.25 | 0.25 | 0.0 |
| persistence | 0.5 | 0.5 | 0.5 |
| contradiction | 0.25 | 0.75 | 0.75 |

### Basis
- Validation. Ozone: international assessment existed; the Antarctic hole (Farman et al., May 1985) was observed but not attributed to CFCs until later. Climate 1997: IPCC Second Assessment (1995), "balance of evidence suggests a discernible human influence". Climate 2015: IPCC AR5 (2013), human influence "extremely likely" the dominant cause.
- Translation. Ozone: Vienna Convention (March 1985), no targets. Climate 1997: UNFCCC (1992), non-binding aim to return to 1990 levels. Climate 2015: Kyoto second period covered a minority of emissions and was not in force.
- Budget. Ozone: research only. Climate 1997: Global Environment Facility (1991). Climate 2015: Green Climate Fund (capitalised 2014).
- Deployment. Ozone: CFC-11 + CFC-12 production 646,642 t (1979) to 694,462 t (1984), +7.4% (AFEAS production table, via unfccc.int; compiled after the decision from producers' own reports). Climate 1997: world CO2 23.21 to 24.23 Gt (1991-1996), +4.4%. Climate 2015: 31.51 to 35.47 Gt (2009-2014), +12.5% (both from data/owid_annual_co2_emissions.csv).
- Contradiction. Ozone: no CFC subsidies known. Climate: fossil-fuel subsidies were documented by the 1990s (e.g. OECD and World Bank estimates; **specific report not verified**) and by 2015 (IEA estimates; **not verified here**).

## Known weaknesses, stated before running
- The rules were written by someone who knows the outcomes; the level boundaries could be chosen to favour the expected result. They were written once, here, before any run.
- Four values rest on sources dated after the decision or unverified (marked above).
- Ozone n uses production; climate n uses emissions.

## C. Held-out case: leaded petrol, decision date 2002-09
Decision point: launch of the UNEP Partnership for Clean Fuels and Vehicles at the Johannesburg summit. Outcome known to the authors: global phase-out completed in 2021. Inputs use the same rules as above and were written before the single run.

### Structure inputs
| Input | Value | Basis |
|---|---|---|
| n_major_actors | 117 | UNEP: "At the time of its formation in 2002, 117 countries world-wide were still using leaded petrol." No consumption data by country was found, so the 80% rule cannot be applied; 117 is the upper bound (**rule not applied: flagged**). Sensitivity: 30. |
| substitutes | 0.75 | Lovei, World Bank Environment Dept. Paper 040 (Aug 1996): phasing out lead costs "US$ 0.01-0.02 per liter of gasoline in the majority of refining capacity". Comparable cost for most uses; older engines needing valve protection keep it below 1. |
| economic_share | 0.001 | Lovei (1996): one significant international supplier of lead additives (Associated Octel). No market value found; 0.1% of world GDP is set as an upper bound (**unverified**). |

### Bottleneck profile
| Score | Value | Basis |
|---|---|---|
| validation | 1.0 | Lead toxicity was settled science well before 2002. |
| translation | 0.5 | Dakar Declaration (June 2001): non-binding target for sub-Saharan Africa; no global instrument. |
| budget | 0.25 | Technical assistance (World Bank Clean Air Initiative) but no dedicated fund before the partnership. |
| deployment | 0.75 | Leaded use falling 10-50% over 1997-2001: large users had banned it (EU, China, India around 2000). No global volume series found (**unverified**). Sensitivity: 1.0. |
| persistence | 0.5 | As for all cases. |
| contradiction | 0.25 | No subsidies to lead additives found. General fuel subsidies in some user countries are not subsidies to lead (**judgement, flagged**). |

### Criteria (same as the protocol)
- Discrimination: predicted gain for leaded petrol 2002 > climate 1997 (0.126).
- Resemblance: at least 2 of the top 3 in {binding regulation, finance transfer, trade measures, substitute support}.
- Fail if voluntary pledges are in the top 3.

### Concern noted before the run, and a secondary measure
Predicted gain = gap x portfolio quality. A problem that is already half-solved has a small gap, so its predicted gain is small even if the remedy is very likely to work. Leaded petrol in 2002 had a smaller gap than climate (strong validation, deployment under way). The primary criterion may therefore fail for a reason that says nothing about whether RDL can recognise a tractable problem. The primary criterion stays as pre-registered. A secondary measure is added now, before the run: **portfolio quality = predicted gain / gap**, compared with climate 1997. The secondary measure cannot turn a primary fail into a pass.

## D. RDL v0.3 held-out pair (written before the single run; engine frozen at 0749b78)
Note: in v0.3, tractability depends only on the structure inputs; the bottleneck profile sets the remaining gap. The held-out criterion is decided by the structure inputs.

### D1. European sulphur emissions, decision date 1985-07 (Helsinki Protocol)
| Input | Value | Basis |
|---|---|---|
| n_major_actors | 10 | Vestreng et al., Atmos. Chem. Phys. 7:3663 (2007), Table 1, 1980 SO2 by country. Regrouped into 1985 states (USSR, Czechoslovakia, Yugoslavia): 9 states for 80% of 55.3 Tg, with Germany as one; East and West Germany were separate, so 10. With today's borders: 12 (sensitivity). Source dated after the decision; EMEP estimates existed at the time. |
| substitutes | 0.5 | Flue-gas desulphurisation was in commercial use by 1985, and fuel switching (gas, nuclear, low-sulphur oil) was available for part of the uses. No dated cost figure was verified (**unverified**). Sensitivity: 0.25. |
| economic_share | 0.10 | Same rule and source as climate: the activity is burning sulphur-bearing fossil fuels (Enerdata, energy spending about 10% of GDP; **dated after**). Sensitivity: 0.02 (if counted as abatement cost rather than fuel use). |

| Score | Value | Basis |
|---|---|---|
| validation | 0.75 | Damage from long-range transport attributed (Swedish case study to the 1972 Stockholm conference; EMEP monitoring from 1977). |
| translation | 0.5 | LRTAP Convention (1979) without targets; "30% club" non-binding pledge (Ottawa, March 1984). |
| budget | 0.25 | Monitoring (EMEP) only. |
| deployment | 0.75 | European SO2 55.3 Tg (1980) to 48.4 Tg (1985), -12.5% (Vestreng et al. Table 1). |
| persistence | 0.5 | As for all cases. |
| contradiction | 0.75 | Public coal subsidies documented in several emitting states (**specific source not verified**). |

### D2. Chrysotile asbestos, global, decision date 2004-09 (first Rotterdam listing proposal)
| Input | Value | Basis |
|---|---|---|
| n_major_actors | 8 | USGS Circular 1298 (Virta, 2006): "eight countries accounted for 82 percent of world apparent consumption in 2003" (China, Russia, India, Kazakhstan, Ukraine, Thailand, Brazil, Iran). Data year before the decision; publication after. |
| substitutes | 0.5 | Substitutes (fibre cement with PVA or cellulose, other materials) in use in countries with bans (EU ban effective 2005), at higher cost for asbestos-cement products (**cost not verified**). Sensitivity: 0.75. |
| economic_share | 0.001 | World consumption 2.11 Mt in 2003 (USGS); value of dependent goods not found; 0.1% of world GDP set as an upper bound (**unverified**), as for leaded petrol. |

| Score | Value | Basis |
|---|---|---|
| validation | 1.0 | IARC Group 1 carcinogen (all forms, including chrysotile). |
| translation | 0.5 | Binding national bans covering a minority of consumption; ILO Convention 162 (1986) regulates but does not ban. |
| budget | 0.25 | No dedicated fund. |
| deployment | 0.25 | Trend 1998-2003 cannot be computed: USGS revised 1998-2000 estimates between its 2003 and 2006 reports (2000: 1.48 million short tons; 2003: 2.11 Mt). Set to "rising 0-10%" (**unverified**). Sensitivity: 0.5. |
| persistence | 0.5 | As for all cases. |
| contradiction | 0.75 | Government funding of the pro-chrysotile Asbestos/Chrysotile Institute by Canada (**not verified here**). |

### Criteria (from RDL_V03_PROTOCOL.md)
Pass: tractability sulphur 1985 > chrysotile 2004, and sulphur 1985 > climate 1997 (0.182). The pre-stated sensitivity settings are reported; the verdict uses the primary values.
