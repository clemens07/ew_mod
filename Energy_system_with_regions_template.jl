using Pkg
Pkg.activate(joinpath(@__DIR__, "."))
Pkg.develop(path=joinpath(@__DIR__, "Dashboard"))
Pkg.instantiate()

using Plots
using JuMP # building models
using DataStructures # using dictionaries with a default value
using HiGHS # solver for the JuMP model
using CSV # readin of CSV files
using DataFrames # data tables
using JSON3
using Dashboard
include(joinpath(@__DIR__, "colors.jl")) # colors for the plots

data_dir = joinpath(@__DIR__, "data")

### Read in of parameters ###
# We define our sets from the csv files
technologies = readcsv("technologies.csv", dir=data_dir).technology
fuels = readcsv("fuels.csv", dir=data_dir).fuel
hour = 1:120
n_hour = length(hour)
storages = readcsv("storages.csv", dir=data_dir).storage


# Also, we read our input parameters via csv files
Demand = readin("demand.csv", default=0, dims=1, dir=data_dir)
OutputRatio = readin("outputratio.csv", dims=2, dir=data_dir)
InputRatio = readin("inputratio.csv", dims=2, dir=data_dir)
VariableCost = readin("variablecost.csv", dims=1, dir=data_dir)
InvestmentCost = readin("investmentcost.csv", dims=1, dir=data_dir)
EmissionRatio = readin("emissionratio.csv", dims=1, dir=data_dir)
DemandProfile = readin("demand_timeseries.csv", default=1/n_hour, dims=2, dir=data_dir)
MaxCapacity = readin("maxcapacity.csv",default=999,dims=1, dir=data_dir)
TagDispatchableTechnology = readin("tag_dispatchabletechnology.csv",dims=1, dir=data_dir)
CapacityFactor = readin("capacity_factors.csv",default=0, dims=2, dir=data_dir)
for t in technologies
    if TagDispatchableTechnology[t] > 0
        for h in hour
            CapacityFactor[t,h] = 1
        end
    end
end

InvestmentCostStorage = readin("investmentcoststorage.csv",dims=1, dir=data_dir)
E2PRatio = readin("e2pratio.csv",dims=1, dir=data_dir)
StorageChargeEfficiency = readin("storagechargeefficiency.csv",dims=2, dir=data_dir)
StorageDisChargeEfficiency = readin("storagedischargeefficiency.csv",dims=2, dir=data_dir)
MaxStorageCapacity = readin("maxstoragecapacity.csv",default=999,dims=1, dir=data_dir)
StorageLosses = readin("storagelosses.csv",default=1,dims=2, dir=data_dir)

# our emission limit
EmissionLimit = 10000

# instantiate a model with an optimizer
ESM = Model(HiGHS.Optimizer)

# this creates our variables
@variable(ESM,TotalCost[technologies]>=0)
@variable(ESM,Production[hour,technologies, fuels] >= 0)
@variable(ESM,Capacity[technologies] >=0)
@variable(ESM,Use[hour,technologies, fuels] >=0)
@variable(ESM,Emissions[technologies] >=0)
@variable(ESM,Curtailment[hour,fuels] >=0)

@variable(ESM,StorageEnergyCapacity[s=storages,f=fuels; StorageDisChargeEfficiency[s,f]>0]>=0)
@variable(ESM,StorageCharge[s=storages, hour, f=fuels; StorageDisChargeEfficiency[s,f]>0]>=0)
@variable(ESM,StorageDischarge[s=storages, hour, f=fuels; StorageDisChargeEfficiency[s,f]>0]>=0)
@variable(ESM,StorageLevel[s=storages, hour, f=fuels; StorageDisChargeEfficiency[s,f]>0]>=0)
@variable(ESM,TotalStorageCost[storages] >= 0)


## constraints ##
# Generation must meet demand
@constraint(ESM, DemandAdequacy[h in hour,f in fuels],
    sum(Production[h,t,f] for t in technologies) + sum(StorageDischarge[s,h,f] for s in storages if StorageDisChargeEfficiency[s,f]>0) == 
        Demand[f]*DemandProfile[f,h] + sum(Use[h,t,f] for t in technologies)+Curtailment[h,f] + sum(StorageCharge[s,h,f] for s in storages if StorageChargeEfficiency[s,f] > 0)
)

# calculate the total cost
@constraint(ESM, ProductionCost[t in technologies],
    sum(Production[h,t,f] * VariableCost[t] for f in fuels, h in hour) + sum(Capacity[t] * InvestmentCost[t]) == TotalCost[t]
)

# limit the production by the installed capacity
@constraint(ESM, ProductionFuntion_disp[h in hour, t in technologies, f in fuels;TagDispatchableTechnology[t]>0],
    OutputRatio[t,f] * Capacity[t] * CapacityFactor[t,h] >= Production[h,t,f]
)
# for variable renewables, the production needs to be always at maximum
@constraint(ESM, ProductionFunction_res[h in hour, t in technologies, f in fuels; TagDispatchableTechnology[t]==0], 
    OutputRatio[t,f] * Capacity[t] * CapacityFactor[t,h] == Production[h,t,f]
)

# define the use by the production
@constraint(ESM, UseFunction[h in hour,t in technologies, f in fuels],
    InputRatio[t,f] * sum(Production[h,t,ff]/OutputRatio[t,ff] for ff in fuels if OutputRatio[t,ff]>0) == Use[h,t,f]
)

# define the emissions
@constraint(ESM, TechnologyEmissions[t in technologies],
    sum(Production[h,t,f] for f in fuels, h in hour) * EmissionRatio[t] == Emissions[t]
)

# limit the emissions
@constraint(ESM, TotalEmissionsFunction,
    sum(Emissions[t] for t in technologies) <= EmissionLimit
)

# installed capacity is limited by the maximum capacity
@constraint(ESM, MaxCapacityFunction[t in technologies],
     Capacity[t] <= MaxCapacity[t]
)

# storage charge is limited by storage energy capacity and E2PRatio
@constraint(ESM, StorageChargeFunction[s in storages, h in hour, f in fuels; StorageDisChargeEfficiency[s,f]>0], 
    StorageCharge[s,h,f] <= StorageEnergyCapacity[s,f]/E2PRatio[s]
)

# storage discharge is limited by storage energy capacity and E2PRatio
@constraint(ESM, StorageDischargeFunction[s in storages, h in hour, f in fuels; StorageDisChargeEfficiency[s,f]>0], 
    StorageDischarge[s,h,f] <= StorageEnergyCapacity[s,f]/E2PRatio[s]
)

# storage level depends on previous period's storage level and current period charge/discharge
@constraint(ESM, StorageLevelFunction[s in storages, h in hour, f in fuels; h>1 && StorageDisChargeEfficiency[s,f]>0], 
    StorageLevel[s,h,f] == StorageLevel[s,h-1,f]*StorageLosses[s,f] + StorageCharge[s,h,f]*StorageChargeEfficiency[s,f] - StorageDischarge[s,h,f]/StorageDisChargeEfficiency[s,f]
)

# storage level for first period does not depend on previous level but we set it to 50% energy capacity
@constraint(ESM, StorageLevelStartFunction[s in storages, h in hour, f in fuels; h==1 && StorageDisChargeEfficiency[s,f]>0], 
    StorageLevel[s,h,f] == 0.5*StorageEnergyCapacity[s,f]*StorageLosses[s,f] + StorageCharge[s,h,f]*StorageChargeEfficiency[s,f] - StorageDischarge[s,h,f]/StorageDisChargeEfficiency[s,f]
)

# storage level is limited by storage capacity
@constraint(ESM, MaxStorageLevelFunction[s in storages, h in hour, f in fuels; StorageDisChargeEfficiency[s,f]>0], 
    StorageLevel[s,h,f] <= StorageEnergyCapacity[s,f]
)

# storage cost are the sum of all storage technology costs
@constraint(ESM, StorageCostFunction[s in storages], 
    TotalStorageCost[s] == sum(StorageEnergyCapacity[s,f]*InvestmentCostStorage[s] for f in fuels if StorageDisChargeEfficiency[s,f]>0)
)

# storage level at the end of a year has to equal storage level at the beginning of year
@constraint(ESM, StorageAnnualBalanceFunction[s in storages, f in fuels; StorageDisChargeEfficiency[s,f]>0], 
    StorageLevel[s,n_hour,f] == 0.5*StorageEnergyCapacity[s,f]
)

# storage capacity is limited by max storage capacity
@constraint(ESM, StorageMaxCapacityConstraint[s in storages], 
    sum(StorageEnergyCapacity[s,f] for f in fuels if StorageDisChargeEfficiency[s,f]>0) <= MaxStorageCapacity[s]
)

# the objective function
# total costs should be minimized
@objective(ESM, Min,
    sum(TotalCost[t] for t in technologies)
    + sum(TotalStorageCost[s] for s in storages)
)

# this starts the optimization
# the assigned solver (here Clp) will takes care of the solution algorithm
optimize!(ESM)
# reading our objective value
objective_value(ESM)

# some result analysis
value.(Production)
value.(Capacity)
value.(StorageEnergyCapacity)
value.(StorageDischarge)
value.(StorageLevel)
value.(StorageCharge)
value.(TotalStorageCost)

df_production = DataFrame(Containers.rowtable(value,Production; header = [:Hour, :Technology, :Fuel, :value]))
df_use = DataFrame(Containers.rowtable(value,Use; header = [:Hour, :Technology, :Fuel, :value]))
df_capacity = DataFrame(Containers.rowtable(value,Capacity; header = [:Technology, :value]))

df_storage_production = DataFrame(Containers.rowtable(value,StorageDischarge; header = [:Technology, :Hour, :Fuel, :value]))
df_storage_charge = DataFrame(Containers.rowtable(value,StorageCharge; header = [:Technology, :Hour, :Fuel, :value]))
df_storage_level = DataFrame(Containers.rowtable(value,StorageLevel; header = [:Technology, :Hour, :Fuel, :value]))

df_demand = DataFrame(
    (Hour=h, Fuel=f, value=Demand[f]*DemandProfile[f,h]) for f in fuels, h in hour
)

append!(df_use, df_storage_charge)
append!(df_production, df_storage_production)
