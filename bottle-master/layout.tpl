

  <head>
  	<!-- Using the bootstrap CSS library -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
    <script src="script.js"></script>
    <style>
* {
  box-sizing: border-box;
}

body {
  font: 16px Arial;
}

.autocomplete {
  /*the container must be positioned relative:*/
  position: relative;
  display: inline-block;
}

input {
  border: 1px solid transparent;
  background-color: #f1f1f1;
  padding: 10px;
  font-size: 16px;
}

input[type=text] {
  background-color: #f1f1f1;
  width: 100%;
}

input[type=submit] {
  background-color: DodgerBlue;
  color: #fff;
  cursor: pointer;
}

.autocomplete-items {
  position: absolute;
  border: 1px solid #d4d4d4;
  border-bottom: none;
  border-top: none;
  z-index: 99;
  /*position the autocomplete items to be the same width as the container:*/
  top: 100%;
  left: 0;
  right: 0;
}

.autocomplete-items div {
  padding: 10px;
  cursor: pointer;
  background-color: #fff;
  border-bottom: 1px solid #d4d4d4;
}

.autocomplete-items div:hover {
  /*when hovering an item:*/
  background-color: #e9e9e9;
}

.autocomplete-active {
  /*when navigating through the items using the arrow keys:*/
  background-color: DodgerBlue !important;
  color: #ffffff;
}
</style>
  </head>
  <body style="background-color:black;">
<div class="container-fluid">
<a href={{"http://" + IP_ADDRESS + "/"}}><button id="place" type="button" class="btn btn-primary">Back To Search</button></a>
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
		    <a href={{"http://" + IP_ADDRESS + "/"}}><button id="login" type="button" class="btn btn-primary">Log In</button></a>
		</div>
	</div>
    </div>

		<form action="/" method="post" class="col-lg-6 offset-lg-3" autocomplete="off" >
			<div class="row justify-content-center">
			    <div class="autocomplete">
				<input id = "myInput" name="search" type="text" autocomplete="off" placeholder="Enter query" />
				</div>
				<span class="input-group-btn">
					<input class="btn btn-primary mb-2" value="Search Nearest Place" type="submit" />
				</span>
			</div>
		</form>
		</div>
  </body>

