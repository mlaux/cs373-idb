

function numCommits() {

	var MattCount = 0;
	var AsadCount = 0;
	var ChidiCount = 0;
	var BradenCount = 0;
	var JeffCount = 0;
	var KevinCount = 0;

	var gitapi = new XMLHttpRequest();
	gitapi.open("GET", "https://api.github.com/repos/mlaux/cs373-idb/commits", false);
	gitapi.send();

	var obj = JSON.parse(gitapi.responseText);

	for(i = 0; i < obj.length; i++) {
	    if (obj[i].commit.author.name == "Matt Laux")
	      MattCount += 1;
	  	else if (obj[i].commit.author.name == "Asad Valliani")
	      AsadCount += 1;
	  	else if (obj[i].commit.author.name == "ChidiOmen")
	      ChidiCount += 1;
	  	else if (obj[i].commit.author.name == "bstotmeister" || obj[i].commit.author.name == "Braden Stotmeister")
	      BradenCount += 1;
	  	else if (obj[i].commit.author.name == "Jeff Taube")
	      AsadCount += 1;
	  	else if (obj[i].commit.author.name == "Kevin Ong")
	      KevinCount += 1;
	}

	totalCommits = MattCount + AsadCount + ChidiCount + BradenCount + JeffCount + KevinCount;
	document.getElementById("mattCommits").innerHTML = MattCount;	
	document.getElementById("chidiCommits").innerHTML = ChidiCount;	
	document.getElementById("bradenCommits").innerHTML = BradenCount;	
	document.getElementById("jeffCommits").innerHTML = JeffCount;	
	document.getElementById("kevinCommits").innerHTML = KevinCount;	
	document.getElementById("asadCommits").innerHTML = AsadCount;	
	document.getElementById("totalCommits").innerHTML = totalCommits;	
}

function numIssues(){
	var count = 1;
	var url = "https://api.github.com/repos/mlaux/cs373-idb/issues/" + count;
	var issuesapi = new XMLHttpRequest();
	issuesapi.open("GET", url, false);
	issuesapi.send();
	var issues = JSON.parse(issuesapi.responseText);

	mattIssues = 0;
	bradenIssues = 0;
	asadIssues = 0;
	kevinIssues = 0;
	chidiIssues = 0;
	jeffIssues = 0;

	while(issues.message != "Not Found"){

		if (issues.user.login == "mlaux")
			mattIssues += 1;
		else if (issues.user.login == "bstotmeister" || issues.user.login == "bradenstotmeister")
			bradenIssues += 1;
		else if (issues.user.login == "asad988")
			asadIssues += 1;
		else if (issues.user.login == "KevinP0ng")
			kevinIssues += 1;
		else if (issues.user.login == "ChidiOmen")
			chidiIssues += 1;
		else if (issues.user.login == "jtaubejr")
			jeffIssues += 1;

		count += 1;
		url = "https://api.github.com/repos/mlaux/cs373-idb/issues/" + count;
		issuesapi.open("GET", url, false);
		issuesapi.send();
		issues = JSON.parse(issuesapi.responseText);

	}

	document.getElementById("totalIssues").innerHTML = count - 1;
	document.getElementById("mattIssues").innerHTML = mattIssues;
	document.getElementById("bradenIssues").innerHTML = bradenIssues;
	document.getElementById("asadIssues").innerHTML = asadIssues;
	document.getElementById("kevinIssues").innerHTML = kevinIssues;
	document.getElementById("chidiIssues").innerHTML = chidiIssues;
	document.getElementById("jeffIssues").innerHTML = jeffIssues;
}

// console.log(gitapi.status);
// console.log(gitapi.statusText);

