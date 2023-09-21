using Dash
using CSV
using DataFrames
using JSON3

# http://127.0.0.1:8050

power_tech = ["SolarPV", "GasPowerPlant", "WindOnhore", "WindOffshore", "Demand", "Power2Gas", "ElectricHeater"]
heat_tech = ["GasCHPPlant", "ElectricHeater", "Demand"]
coal_tech = ["Demand"]
gas_tech = ["GasExtractor", "Demand", "GasPowerPlant", "GasCHPPlant", "LPGCar"]
h2_tech = ["Power2Gas", "Demand", "H2Tank", "H2Tank"]
mobility_tech = ["LPGCar"]

capacity = CSV.read("./results/capacity.csv", DataFrame)
production = CSV.read("./results/production.csv", DataFrame)
colors = JSON3.read("./results/colors.json")
technologies = CSV.read("./data/technologies.csv", DataFrame)

production_power = filter(:Fuel => n -> n == "Power", production)

transform!(technologies, "technology" => ByRow(x-> colors[x]) => "Color")

data_p1 = []
data_p2 = []

for tech in eachrow(technologies)
    production_power_tech = filter(:Technology => n -> n == tech.technology, production_power)
    push!(data_p1, (x = production_power_tech.Hour, y = production_power_tech.value, type = "line", name=tech.technology, fill="tozero", stackgroup="one"))
end

for tech in eachrow(technologies)
    production_power_tech = filter(:Technology => n -> n == tech.technology, production_power)
    push!(data_p2, (x = capacity.Technology, y = capacity.value, type = "bar", color = technologies.Color, name=tech.technology))
end


app = dash()

app.layout = html_div(children=[
    # All elements from the top of the page
    html_div([
        html_h1(children="Hello Dash"),
        html_div("Dash: A web application framework for your data."),
        dcc_graph(
            id = "example-graph-1",
            figure = (
                data = [
                    (x = ["giraffes", "orangutans", "monkeys"], y = [20, 14, 23], type = "bar", name = "SF"),
                    (x = ["giraffes", "orangutans", "monkeys"], y = [12, 18, 29], type = "bar", name = "Montreal"),
                ],
                layout = (title = "Dash Data", barmode="group"),
            )
        ), 
    ]),
    
    html_div([
    html_h1("Dispatch Power"),
    dcc_checklist(
        id="checklist",
        options=["Asia", "Europe", "Africa","Americas","Oceania"],
        value=["Americas", "Oceania"],
        inline=true
        ),
    ]),
    
    html_div([
        html_h1(children="Dispatch"),
        dcc_graph(
            id = "Dispatch",
            figure = (
                data = data_p1,
            ),
        ),
    ]),
    
    
    # New Div for all elements in the new 'row' of the page
    html_div([
        html_h1(children="Installed Capacity"),
        dcc_graph(
            id = "installed_capacity",
            figure = (
                data = data_p2
            ),
        ),
    ]),
])



# html_div() do
#     html_h1("Hello Dash"),
#     html_div("Dash: A web application framework for your data."),
#     dcc_graph(
#         id = "example-graph-1",
#         figure = (
#             data = [
#                 (x = ["giraffes", "orangutans", "monkeys"], y = [20, 14, 23], type = "bar", name = "SF"),
#                 (x = ["giraffes", "orangutans", "monkeys"], y = [12, 18, 29], type = "bar", name = "Montreal"),
#             ],
#             layout = (title = "Dash Data", barmode="group")
#         )
#     )
#     html_h1("Bye Dash"),
#     dcc_graph(
#         id = "example-graph-2",
#         figure = (
#             data = [
#                 (x = ["giraffes", "orangutans", "monkeys"], y = [20, 14, 23], type = "bar", name = "SF"),
#                 (x = ["giraffes", "orangutans", "monkeys"], y = [12, 18, 29], type = "bar", name = "Montreal"),
#             ],
#             layout = (title = "Dash Data", barmode="group")
#         )
#     )
# end

run_server(app, "0.0.0.0", debug=true)