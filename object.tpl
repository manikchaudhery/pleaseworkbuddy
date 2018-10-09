<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>
</head>
<body>
	<br>
	<h2>Results</h2>
	<br><br>
	<table class="table table-hover table-dark">
	  <tr>
	    <th>Word</th>
	    <th>Frequency</th>
	  </tr>
	% for k, v in occurences.items():
	    <tr>
		<td>{{k}}</td>
		<td>{{v}}</td>
	    </tr>
	% end
	</table>
</body>



