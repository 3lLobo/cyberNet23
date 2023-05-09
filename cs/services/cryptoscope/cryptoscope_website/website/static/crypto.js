$(document).ready(function() {

    $(".pricechart").on("click", handle_pricechart_click);

    show_toast_containers();

    update_overview_chart();

    update_price_charts(); 

    update_account_transaction_table();

    update_symbol_transaction_table(); });

// redirect to details page when symbol clicked 

function handle_pricechart_click(event) {

    event.preventDefault();

    var symbol = $(this).data("symbol");

    window.location = "/detail?symbol=" + encodeURIComponent(symbol);

    return false;
}

// update overview chart when present in the document

function update_overview_chart() {

    var element = $(".overviewchart");

    if(!element.length) return false;

    var data = element.data("overview-data");

    Highcharts.chart(element[0], { 

        accessibility: { enabled: false },

        chart: { type: "column", backgroundColor: null, options3d: { enabled: true, alpha: 0, beta: 0, depth: 70 } },

        credits: { enabled: false },

        title: { text: "Transaction Overview" },

        xAxis: { categories: Object.keys(data) },

        yAxis: { title: { text: "Transaction Count" } },

        legend: { enabled: false },

        tooltip:{ headerFormat: "" },

        plotOption: { column: { depth: 25 } },

        series: [{ name: "Transactions", data: Object.values(data) }]
    });


    return true;
}

// update all the price-chart information when present

function update_price_charts() {

    $(".pricechart").each(function() {

        var element = this;

        var price_points = $(this).data("price-data").split(/,/);

        var current_time = Math.floor(Date.now() / 1000);

        var chart_data = [];

        price_points.forEach(function(element, index) { 

            chart_data.push(parseInt(element)); });

        Highcharts.chart(element, { 

            accessibility: { enabled: false },

            chart: { zoomType: "x", backgroundColor: "none" },

            credits: { enabled: false },

            title: { text: $(element).data("symbol"), align: "center" },

            xAxis: { labels: { enabled: false }, visible: false },

            yAxis: { title: { text: "EUR" } },

            legend: { enabled: false },

            tooltip:{ headerFormat: "", valuePrefix: "€"},

            series: [{ 

                type: "line", 

                name: $(element).data("name"),

                data: chart_data 

            }] } )
    })

    return true;
}

// render symbol_transaction table present in the document

function update_symbol_transaction_table() {

    var table = $(".symbol_transaction_table");

    if(!table.length) return false;

    $.post("/detail", { _xsrf: xsrf_token, symbol: table.data("symbol") }, 

        function(result) {

            if(!result.hasOwnProperty("transactions")) return false;

            result["transactions"].forEach(function(transaction) {

                var record = $("<tr/>");

                record.append($("<td/>").text(transaction["index"]));

                record.append($("<td/>").text(transaction["symbol"]));

                record.append($("<td/>").text(transaction["src"]));

                record.append($("<td/>").text(transaction["dst"]));

                record.append($("<td/>").text(transaction["amount"]));

                $("tbody", table).append(record); }); 
        });

    return true;
}

// render account_transaction table present in the document

function update_account_transaction_table() {

    var table = $(".account_transaction_table");

    if(!table.length) return false;

    $.post("/account", { _xsrf: xsrf_token, username: table.data("username") }, 

        function(result) {

            if(!result.hasOwnProperty("transactions")) return false;

            result["transactions"].forEach(function(transaction) {

                var record = $("<tr/>");

                record.append($("<td/>").text(transaction["index"]));

                record.append($("<td/>").text(transaction["symbol"]));

                record.append($("<td/>").text(transaction["src"]));

                record.append($("<td/>").addClass("text-truncate").text(transaction["src_wallet"]));

                record.append($("<td/>").text(transaction["dst"]));

                record.append($("<td/>").addClass("text-truncate").text(transaction["dst_wallet"]));

                record.append($("<td/>").text(transaction["amount"]));

                $("tbody", table).append(record); }); 
        });

    return true;
}

// show toast containers visible in the document

function show_toast_containers() {

	$(".toast").each(function() {

		var element = this;

		var show_once_key = $(this).data("show-once-key");

		if(show_once_key) {

			if(sessionStorage.getItem(show_once_key)) return true;
		
			sessionStorage.setItem(show_once_key, true);	
		}

 	  	bootstrap.Toast.getOrCreateInstance(element).show(); });

    return true;
}
