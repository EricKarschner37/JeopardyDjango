const socket = new WebSocket("wss://" + window.location.host + "/ws/buzzer/server/");

$(document).ready(function(){
    $("div#clue_div").css("height", $("table#clue_table").css("height"));
    $("div#clue_div").css("width", $("table#clue_table").css("width"));

    $(document).delegate("div#clue_div", "click", function(){
        if ($(this).attr("status") == "clue"){
            $(this).attr("status", "answer");
            $(this).find("p.answer").css("visibility", "visible");

			let request = {};
			request.request = "answer";
			socket.send(JSON.stringify(request));
        } else if ($(this).attr("status") == "double"){
            $(this).attr("status", "clue");
            $(this).find("p.clue").css("visibility", "visible");
            $(this).find("p.double").css("visibility", "hidden");
        } else if ($(this).attr("status") == "answer"){
            $(this).find("p.answer").css("visibility", "hidden");
            $(this).find("p.clue").css("visibility", "hidden");

            $(this).attr("status", "done");
            $(this).css("display", "none");
            $("table#clue_table").css("display", "block");

			let request = {};
			request.request = "idle";
			socket.send(JSON.stringify(request));
        }
    });

	
	socket.addEventListener('message', function(e) {
		let json = JSON.parse(e.data);

		if (json.message === "state"){
			for (let [name, balance] of Object.entries(json.players)){
				showPlayer(name, balance);
			}

			if (json.state === "daily_double"){
				showDailyDouble();
			} else if (json.state === "buzzed"){
				playerBuzzed(json.player);
			} else if (json.state === "question"){
				showQuestion(json.clue, json.answer, json.cost);
			}
		} else if (json.message === "categories"){
			ReactDOM.render(
				React.createElement(
					ClueBoard,
					{categories: json.categories}
				),
				document.getElementById("clue_table_container")
			);
			console.log("Render completed")
		}
	});
});

function revealClue(row, col){
	let request = {};
	request.request = "reveal";
	request.row = row;
	request.col = col;

	socket.send(JSON.stringify(request))
}

function showPlayer(name, balance) {
	_name = name.split(" ").join("_");

	if ($("table.info").find("tr#" + _name + "_info").length){
		$("table.info").find("tr#" + _name + "_info").find("td.balance").text("$" + balance);
	} else {
		$("table.info").append('<tr id="' + _name + '_info"><td align="left">' + name + '</td><td align="right" class="balance">$' + balance.toString() + '</td></tr>');
	}

	$("table.info").find("tr#" + name.split(" ").join("_") + "_info").removeClass("buzz");
}

function showCategories(categories){
	for (i=0; i<6; i++){
		$("table#clue_table").find("p#category_" + i.toString()).text(categories[i]);
	}
}

function showDailyDouble(){
	$("div#clue_div").find("p.double").css("visibility", "visible");
	$("div#clue_div").find("p.cost").text("$???");
	$("div#clue_div").css("display", "block");
	$("table#clue_table").css("display", "none");
}

function removePlayer(name){
	$("tr#" + name.split(" ").join("_") + "_info").remove();
}

function playerBuzzed(name){
	$("table.info").find("tr#" + name.split(" ").join("_") + "_info").addClass("buzz");
}

function showQuestion(clue, answer, cost){
	$("div#clue_div").find("p.double").css("visibility", "hidden");
	$("div#clue_div").find("p.clue").text(clue);
	$("div#clue_div").find("p.answer").text(answer);
	$("div#clue_div").find("p.cost").text("$" + cost.toString());

	$("div#clue_div").find("p.clue").css("visibility", "visible");
	$("div#clue_div").attr("status", "clue");

	$("div#clue_div").css("display", "block");
	$("table#clue_table").css("display", "none");
}
