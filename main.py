import PySimpleGUI as sg
import priceimport
import availabilityimport
import killorder
import findmerchant
import exceltojson
import product

# sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()

layout = [
    [sg.Text("Choose operation")],
    [sg.Button("Kill orders", key="kill")],
    [sg.Button("Create Price import file", key="price")],
    [sg.Button("Create Availability import file", key="availability")],
    [sg.Button("Find merchant name from API key", key="findmerchant")],
    [sg.Button("Create JSON from Excel", key="exceltojson")],
    [sg.Button("Product", key="product")],
    [sg.Button("Exit")]
]

window = sg.Window("Tech support small toolz", layout)

while True:
    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    match event:
        case "kill":
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
        case "product":
            product.product_main()


window.close()