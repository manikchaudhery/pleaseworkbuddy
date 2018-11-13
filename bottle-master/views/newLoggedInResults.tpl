<head>
	<!-- Using the bootstrap CSS library -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>
</head>

<div class="text-center">
    <h3> Welcome {{user_email}} </h3>
    <br>
    <p class="h1">Kuria</p>
    <br><a href="http://184.73.52.206/logout"><button id="logout" type="button" class="btn">Log Out</button></a>

</div>
<form action="/redirect" method="post" class="col-lg-6 offset-lg-3 ">
	<div class="row justify-content-center">
		<input name="search" type="text" placeholder="Enter query" />
		<span class="input-group-btn">
			<input class="btn btn-primary mb-2" value="Search" type="submit" />
		</span>
	</div>
</form>
<div class="row">
    % i = 0
	<div class="col-md-4"></div>
	<div class="col-md-4">
		<h2 class="text-center">Results</h2>
		<table class="table table-hover table-dark">
			<tr>
				<th>URL</th>
			</tr>
				% for item in urlsList:
					<tr>
						<td><a href="{{item}}">{{item}}</a></td>
						% i = i+1
					</tr>
				% end
			</table>
	</div>
	<div class="col-md-4">
	</div>
</div>

<div class="text-center">
        % newPrevString =  "http://184.73.52.206/resultsLoggedIn/" + str(previousPage)
        <a href={{newPrevString}}><button id="previous" type="button" class="btn"><<</button></a>
        % newString =  "http://184.73.52.206/resultsLoggedIn/" + str(nextPage)
        <a href= {{newString}}><button id="next" type="button" class="btn">>></button></a>
</div>


<div class="text-center">
    <h5>Page {{currentPage}} of {{pagesNeeded}}</h5>
</div>

