import PySimpleGUI as sg
import priceimport
import availabilityimport
import killorder
import findmerchant
import exceltojson
import fortesting
import checkprice
import createavailability
import dynamicmodule
import parser

# sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()
tooltips = {"kill": "Takes a list of orders and cancels or marks them as returned depending on status",
            "price": "Creates a price import file based on an inventory report",
            "availability": "Creates an availability file based on an inventory report",
            "custom_availability": "Creates an availability file but with chosen delivery times",
            "findmerchant": "Takes an API key and returns the source id for the merchant",
            "exceltojson": "Converts Excel files to JSON files",
            "checkprice": "Compares price between imported price file and prices from an inventory report",
            "parser": "Takes a list of CDON product links and parses out the product id",
            "dynamic": "This is a dynamic module that I change based on needs",
            "testing": "This is just a module for testing, DO NOT USE"
            }
# noinspection PyUnresolvedReferences
layout = [
    [sg.Text("Choose operation")],
    [sg.Button("Kill orders", key="kill", tooltip=tooltips.get("kill"))],
    [sg.Button("Create Price import file", key="price", tooltip=tooltips.get("price"))],
    [sg.Button("Create Availability import file", key="availability", tooltip=tooltips.get("availability"))],
    [sg.Button("Create custom availability", key="custom_availability", tooltip=tooltips.get("custom_availability"))],
    [sg.Button("Find merchant name from API key", key="findmerchant", tooltip=tooltips.get("findmerchant"))],
    [sg.Button("Create JSON from Excel", key="exceltojson", tooltip=tooltips.get("exceltojson"))],
    [sg.Button("Check price", key="checkprice", tooltip=tooltips.get("checkprice"))],
    [sg.Button("Link parser", key="parser", tooltip=tooltips.get("parser"))],
    [sg.Button("Dynamic", key="dynamic", tooltip=tooltips.get("dynamic"))],
    [sg.Button("Testing", key="testing", tooltip=tooltips.get("testing"))],
    [sg.Button("Exit")]
]

# noinspection PyUnresolvedReferences
window = sg.Window("Tech support small toolz", layout)

while True:
    event, values = window.read()

    # noinspection PyUnresolvedReferences
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    match event:
        case "dynamic":
            dynamicmodule.dynamic_main()
        case "custom_availability":
            createavailability.custom_availability_main()
        case "kill":
            # noinspection PyUnresolvedReferences
            api_key = sg.popup_get_text("Please enter the API KEY", "Getting API KEY", default_text="")
            killorder.kill_order_main(api_key)
            sg.popup("Orders have been processed! See terminal for more information.")
        case "price":
            amount = priceimport.price_import_main()
            sg.popup(f"Price file finished\nAmount of products in XML file: {amount}")
        case "availability":
            availabilityimport.availability_import_main()
        case "findmerchant":
            api_key = sg.popup_get_text("Please enter the API KEY", "Getting API KEY", default_text="")
            merchant = findmerchant.find_merchant_main(api_key)
            if merchant is None:
                sg.popup_get_text("Issue fetching the merchant name\nPlease check the API key for errors",
                                  "Results", default_text=api_key)
            else:
                sg.popup(f"Merchant name: {merchant}")
        case "exceltojson":
            exceltojson.excel_to_json_main()
        case "parser":
            parser.parser_main()
        case "product":
            product.product_main()
        case "testing":
            fortesting.testingmain()
        case "checkprice":
            checkprice.price_main()


window.close()
