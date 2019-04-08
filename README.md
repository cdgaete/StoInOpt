# StorInOpt

This is an small library developed in the context of [BONSAI project](https://bonsai.uno/). The purpose of this library is to make an estimation of electricity consumption of storage electricity options in a electricity market when this information is not available. This is particularly interesting for LCA projects allowing the allocation of  environmental impacts to electricity storage options.

## Input data

The model considers that between dispatches power is consumed for electricity storage. It is assumed that the storage options provide the service of energy arbitrage to the power market. The estimation of electricity consumption of the storage option consists of optimization linear Programming that minimizes the costs of electricity consumed by the storage option. The input parameters  are:

- Electricity dispatched by the storage option.
- Market-Clearing electricity price.

ENTSO-e API is used to obtain information of European electricity markets.


## Pumped hydro storage

Pumped hydro storage is the only storage option that is informed by ENTSO-e API for some European countries (2019). Therefore StorInOpt estimates the consumption of this technology.


### Instructions soon

Install LP solver (clp, glpk, etc...)
