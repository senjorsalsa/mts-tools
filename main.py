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
import manual_parser
import carriers
import checkgtindupe
import deliveryerrors
import convertchar


tooltips = {
            "kill": "Takes a list of orders and cancels or marks them as returned depending on status",
            "price": "Creates a price import file based on an inventory report",
            "availability": "Creates an availability file based on an inventory report",
            "custom_availability": "Creates an availability file but with chosen delivery times",
            "findmerchant": "Takes an API key and returns the source id for the merchant",
            "exceltojson": "Converts Excel files to JSON files",
            "checkprice": "Compares price between imported price file and prices from an inventory report",
            "parser": "Takes a list of CDON product links and parses out the product id",
            "dynamic": "This is a dynamic module that I change based on needs",
            "testing": "This is just a module for testing, DO NOT USE",
            "carriers": "Fetches a list of package carriers and saves to a list",
            "delivery_errors": "Gets 1000 latest imported files and gathers any errors, saves to a file."
            }

# import file shenanigans
import_file_tab = [
    [sg.Text("")],
    [sg.Button("Create Price import file", key="price", tooltip=tooltips.get("price"))],
    [sg.Button("Create Availability import file", key="availability", tooltip=tooltips.get("availability"))],
    [sg.Button("Create custom availability", key="custom_availability", tooltip=tooltips.get("custom_availability"))],
    [sg.Button("Check duplicate GTINs", key="check_gtin_dupe")]
]

other_tab = [
    [sg.Text("")],
    [sg.Button("Generate package carrier list", key="carriers", tooltip=tooltips.get("carriers"))],
    [sg.Button("Delivery errors", key="delivery_errors", tooltip=tooltips.get("delivery_errors"))],
    [sg.Button("Find merchant name from API key", key="findmerchant", tooltip=tooltips.get("findmerchant"))],
    [sg.Button("Create JSON from Excel", key="exceltojson", tooltip=tooltips.get("exceltojson"))],
    [sg.Button("Check price", key="checkprice", tooltip=tooltips.get("checkprice"))],
    [sg.Button("Link parser", key="parser", tooltip=tooltips.get("parser"))],
    [sg.Button("Dynamic", key="dynamic", tooltip=tooltips.get("dynamic"))],
    [sg.Button("Testing", key="testing", tooltip=tooltips.get("testing"))],
    [sg.Button("Convert chars", key="convert_char")]
]

kill_order_tab = [
    [sg.Text("")],
    [sg.Button("Kill orders", key="kill", tooltip=tooltips.get("kill"))]
]

layout = [
    [sg.TabGroup([
        [sg.Tab("Kill orders", kill_order_tab),
         sg.Tab("Import shenanigans", import_file_tab),
         sg.Tab("Other", other_tab)]
    ])],
    [sg.Button("Exit")]
]

window = sg.Window("Tech support small toolz", layout)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        break

    match event:
        case "convert_char":
            convertchar.convert_main()
        case "delivery_errors":
            deliveryerrors.delivery_main()
        case "check_gtin_dupe":
            checkgtindupe.gtin_main()
        case "dynamic":
            dynamicmodule.dynamic_main()
        case "custom_availability":
            createavailability.custom_availability_main()
        case "kill":
            killorder.kill_order_main()
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
            manual_parser.parser_main()
        case "testing":
            fortesting.test_main()
        case "checkprice":
            checkprice.price_main()
        case "carriers":
            carriers.carriers_main()


window.close()
