
var gitapi = new XMLHttpRequest();
gitapi.open("GET", "https://api.github.com/repos/mlaux/cs373-idb/commits", false);
gitapi.send();

var MattCount = 0;
var AsadCount = 0;
var ChidiCount = 0;
var BradenCount = 0;
var JeffCount = 0;
var KevinCount = 0;
function numCommits(){
	for(i = 0; i < gitapi.length; i++) {
	    if (gitapi[i].commit.author.name == "Matt Laux")
	      MattCount += 1;
	  	else if (gitapi[i].commit.author.name == "Asad Valliani")
	      AsadCount += 1;
	  	else if (gitapi[i].commit.author.name == "ChidiOmen")
	      ChidiCount += 1;
	  	else if (gitapi[i].commit.author.name == "bstotmeister" || gitapi[i].commit.author.name == "Braden Stotmeister")
	      BradenCount += 1;
	  	else if (gitapi[i].commit.author.name == "Jeff Taube")
	      AsadCount += 1;
	  	else if (gitapi[i].commit.author.name == "Kevin Ong")
	      KevinCount += 1;
	}
}

totalCommits = MattCount + AsadCount + ChidiCount + BradenCount + JeffCount + KevinCount;
document.getElementById("mattCommits").innerHTML = MattCount;

// console.log(gitapi.status);
// console.log(gitapi.statusText);
