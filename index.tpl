<form action="/" method="post">
	<input name="search" type="text" />
	<input value="Search" type="submit" />
</form>
<style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}
</style>

<h2>History</h2>
<p>{{len(sortedTopTwentyDictionary)}}<p>
<table>
  <tr>
    <th>Word</th>
    <th>Frequency</th>
  </tr>
% for k, v in sortedTopTwentyDictionary.items():
    <tr>
        <td>{{k}}</td>
        <td>{{v}}</td>
    </tr>
% end
</table>


