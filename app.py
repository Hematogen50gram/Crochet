from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# simple in-memory counter (per server, not per user)
decrement = False
row_counter = 0
stitches_counter = 0
current_tab = "Tab 1"
table_data:dict[str,list[dict[str,int]]] = {current_tab:[]}


@app.route("/")
def index():
    return render_template(
        "index.html", counter=row_counter, stitches_counter=stitches_counter
    )
@app.route("/update_row", methods=["POST"])
def update_row():
    global table_data
    global stitches_counter
    global current_tab
    print(f"On row update:{table_data}")
    if decrement:
        table_data[current_tab].pop()
    else:
        row = {"a": row_counter, "b": stitches_counter}
        table_data[current_tab].append(row)
    stitches_counter = 0


    return jsonify({"rows": table_data[current_tab]})

@app.route("/rows", methods=["GET"])
def get_rows():
    return jsonify({"rows": table_data[current_tab]})

@app.route("/update_row_count", methods=["POST"])
def update_row_count():
    global row_counter
    global decrement
    action = request.json.get("action")
    if action == "increment":
        row_counter += 1
        decrement = False
    elif action == "decrement":
        row_counter = max(0, row_counter - 1)
        decrement = True
    print("new counter" + str(row_counter))
    return jsonify({"counter": row_counter})

@app.route("/switch_tab", methods=["POST"])
def switch_tab():
    global current_tab
    global stitches_counter
    global row_counter
    tab_name = request.json.get("tab_name")
    current_tab = tab_name
    stitches_counter = 0
    row_counter = len(table_data[current_tab])
    print(f"Switching tab {current_tab}")
    return jsonify({"current_tab": current_tab})

@app.route("/add_tab",methods=["POST"])
def add_tab():
    global table_data
    tab_name = request.json.get("tab_name")
    print(tab_name)
    table_data[tab_name] = []
    return jsonify({"new_tab": tab_name})

@app.route("/update_stitches", methods=["POST"])
def update_stitches():
    stitches = request.json.get("count")
    global stitches_counter
    if not stitches:
        stitches_counter = 0
    else:
        stitches_counter += stitches
    return jsonify({"count":stitches_counter})

if __name__ == "__main__":
    app.run(debug=True)
