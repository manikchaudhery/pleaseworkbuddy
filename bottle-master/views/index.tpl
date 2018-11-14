<head>
	<!-- Using the bootstrap CSS library -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>
</head>

<div class="text-center">
	<img src="static/logo_transparent.jpg" height="200" width="200">
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
	<div class="col-md-4"></div>
	<div class="col-md-4">
		<h2 class="text-center">Results</h2>
		<table class="table table-hover table-dark">
			<tr>
				<th>Word</th>
				<th>Frequency</th>
			</tr>
				% for item in occurences:
					<tr>
						<td>{{item[0]}}</td>
						<td>{{item[1]}}</td>
					</tr>
				% end
			</table>
	</div>
	<div class="col-md-4">
	</div>
</div>
