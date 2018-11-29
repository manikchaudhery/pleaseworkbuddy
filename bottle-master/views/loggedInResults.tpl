<head>
	<!-- Using the bootstrap CSS library -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>
</head>

<div class="text-center">
    <h3> Welcome {{user_email}} </h3>
    <img src="static/logo_transparent.png" height="200" width="200">
    <br><a href="http://34.194.136.17/logout"><button id="logout" type="button" class="btn">Log Out</button></a>

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
    <h5>Page 1 of 1</h5>
</div>