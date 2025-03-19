import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request

app = Flask(__name__)

# SIP Calculation Function
def calculate_sip(monthly_investment, interest_rate, years):
    n = years * 12
    r = interest_rate / 100 / 12
    future_value = monthly_investment * (((1 + r) ** n - 1) / r) * (1 + r)
    return round(future_value, 2)

# Generate Yearly SIP Data for Graph
def yearly_sip_growth(monthly_investment, interest_rate, years):
    yearly_totals = []
    total_amount = 0
    r = interest_rate / 100 / 12

    for year in range(1, years + 1):
        months = year * 12
        total_amount = monthly_investment * (((1 + r) ** months - 1) / r) * (1 + r)
        yearly_totals.append((year, round(total_amount, 2)))

    return yearly_totals

# Generate and Save Graph
def generate_graph(yearly_data):
    years, amounts = zip(*yearly_data)

    plt.figure(figsize=(8, 5))
    plt.bar(years, amounts, color='skyblue')
    plt.xlabel("Years")
    plt.ylabel("Total Amount (₹)")
    plt.title("SIP Yearly Growth")

    # Save to a buffer
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            monthly_investment = float(request.form["monthly_investment"])
            interest_rate = float(request.form["interest_rate"])
            years = int(request.form["years"])

            final_amount = calculate_sip(monthly_investment, interest_rate, years)
            yearly_data = yearly_sip_growth(monthly_investment, interest_rate, years)
            graph_url = generate_graph(yearly_data)

            return render_template("result.html", monthly_investment=monthly_investment,
                                   interest_rate=interest_rate, years=years,
                                   final_amount=final_amount, graph_url=graph_url)
        except ValueError:
            return render_template("index.html", error="Please enter valid numbers.")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
