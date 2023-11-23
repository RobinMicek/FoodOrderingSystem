/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

    Jakákoliv úprava a distribuce tohoto kódu 
    bez povolení autora je zakázána!

    © Robin Míček 2023 - 2024

********************************************************
*/

// USAGE:
// <div class="m-5">
//      {% with text="Hledat", type="text", name="search" %}
//            {% include "/components/form/input.html" %}
//      {% endwith %}
// </div>
// <div id="datatable" class="m-5">
// <table style="width: 100%;" class="text-center rounded-md shadow-md bg-secondary">
// <thead class="text-white uppercase">
//    <tr id="thead">
//        <th class="px-6 py-4 text-md font-bold text-left"></th>
//    </tr>
// </thead>
// <tbody class="bg-white" id="tbody">            
//        <tr>
//            <td class="px-6 py-4 text-md border-secondary text-left"></td>
//        </tr>
// </tbody>
// </table>
// </div>
// <div id="datatable" class="m-5 rounded-xl"></div>
// <script src="/files/js/createDataTable.js"></script>


function search() {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("datatable");
    tr = table.getElementsByTagName("tr");
    
    // Loop through all table rows, and hide those that don't match the search query
    for (i = 0; i < tr.length; i++) {
        if (tr[i].id != "thead") {
            tr[i].style.display = "none";
        }
        
    }

    for (i = 0; i < tr.length; i++) {
        for (j = 0; j < tr[i].getElementsByTagName("td").length; j++) {
            td = tr[i].getElementsByTagName("td")[j];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                }
            }
        }
    }
}

document.getElementById("search").addEventListener("change", (event => {
    search()
}))