<head>
	<!-- Using the bootstrap CSS library -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>
</head>

<body style="background-color:black;">
<div class="container-fluid">
<div class="row">
	<div class="col-md-4"></div>
	<div class="col-md-4">
		<div class="text-center">
			<img src="https://i.ibb.co/vLHVMLr/logo-transparent.jpg" height="200" width="200">
		</div>
	</div>
	<div class="col-md-4">
		<div class="text-center">
			<br>
		    <a href="http://localhost:8080/login"><button id="login" type="button" class="btn btn-primary">Log In</button></a>
		</div>
	</div>
</div>

<form action="/" method="post" class="col-lg-6 offset-lg-3 ">
	<div class="row justify-content-center">
		<input name="search" type="text" placeholder="Enter query" />
		<span class="input-group-btn">
			<input class="btn btn-primary mb-2" value="Search" type="submit" />
		</span>
	</div>
</form>

<div class="row">
    % i = 0
	<div class="col-md-1"></div>
	<div class="col-md-4">
		<h1 class="text-center"><kbd>Search Results for "{{firstWord}}"</kbd></h1>
		<table class="table table-hover table-dark">
				% for iter in range(len(urlsList)):
					<tr>
						<td>
							<p class="h3 text-primary">{{titlesList[iter]}}</p>
							<p class="h6"><u><a class="text-success" href="{{urlsList[iter]}}">{{urlsList[iter]}}</a>
								</u></p>
							<p class="h5 text-white">{{descriptionList[iter]}}</p>
						</td>
						% i = i+1
					</tr>
				% end
		</table>
		<div class="text-center">
			% newString =  "http://localhost:8080/results/" + str(nextPage)
			<a href= {{newString}}><button id="next" type="button" class="btn">>></button></a>
			<h5><kbd>Page {{currentPage}} of {{pagesNeeded}}</kbd></h5>
		</div>
	</div>
	<div class="col-md-7">
	</div>
</div>
</div>
</body>



<div class="row">
    % i = 0
	<div class="col-md-4"></div>
	<div class="col-md-4">
		<h2 class="text-center">Results</h2>
		<table class="table table-hover table-dark">
				% for item in userTweets:
					<tr>
					    <td>@{{twitterUsers[i]}}</td>
						<td><a href="{{item}}">{{item}}</a></td>
						% i = i+1
					</tr>
				% end
			</table>
	</div>
	<div class="col-md-4">
	</div>
</div>



<div class="row">
% i =0
	<div class="col-md-4"></div>
	<div class="col-md-4">
		<h2 class="text-center">Results</h2>
		<table class="table table-hover table-dark">
				% for item in newsArticlesHeadlines:
					<tr>
					    <td>
					    <p>{{newsArticlesHeadlines[i]}}<p>
					    <p>{{newsArticlesPublishedAt[i]}}<p>
					    <p>{{newsArticlesDescription[i]}}<p>
					    <img src={{newsArticlesImage[i]}}>
					    </td>
                        % i = i+1
					</tr>
				% end
			</table>
	</div>
	<div class="col-md-4">
	</div>
</div>
