<!doctype html>

  <head>
  	<!-- Using the bootstrap CSS library -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
    <script src="script.js"></script>
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

		<form action="/" method="post" class="col-lg-6 offset-lg-3" autocomplete="off" >
			<div class="row justify-content-center">
			    <div class="autocomplete">
				<input id = "myInput" name="search" type="text" autocomplete="off" placeholder="Enter query" />
				</div>
				<span class="input-group-btn">
					<input class="btn btn-primary mb-2" value="Search" type="submit" />
				</span>
			</div>
		</form>
  </body>

