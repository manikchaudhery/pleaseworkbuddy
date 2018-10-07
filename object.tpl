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


<h2>Results</h2>

<table>
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

