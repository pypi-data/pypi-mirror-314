module KM3NeTTestData

export datapath

const DATA_DIR = joinpath(@__DIR__, "..", "km3net_testdata", "data")

datapath(p...) = joinpath(DATA_DIR, p...)

end
