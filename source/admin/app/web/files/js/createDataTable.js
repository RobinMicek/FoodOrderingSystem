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
// <table style="width: 100%" class="text-center rounded-md shadow-md bg-secondary">
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
// <div class="w-full flex justify-end items-center gap-1 p-5">
//    <div>
//        {% with id="pageBack", type="button", icon="las la-angle-left" %}
//            {% include "/components/form/button.html" %}
//        {% endwith %}
//    </div>
//
//    <div id="pageIndicator" class="py-2 px-4 bg-secondary text-white text-xl rounded-md">1/1</div>
//
//    <div>
//        {% with id="pageNext", type="button", icon="las la-angle-right" %}
//            {% include "/components/form/button.html" %}
//        {% endwith %}
//    </div>
//</div>
// <script src="/files/js/createDataTable.js"></script>


// Define a global variable to store the rows
var displayedRows = []
var numPerPage = 10
var currentPage = 1

document.addEventListener("DOMContentLoaded", function () {
    initializeTable()
})

function initializeTable() {
    // Get data from the table
    displayedRows = Array.from(document.getElementById("datatable").getElementsByTagName("tr"))

    showPage(1)
    setupPagination()

    // Add event listener for the search input
    document.getElementById("search").addEventListener("input", function () {
        search()
    })
}


function search() {
    var input, filter, table, tr, td, txtValue
    input = document.getElementById("search")
    filter = input.value.toUpperCase()
    table = document.getElementById("datatable")
    tr = Array.from(table.getElementsByTagName("tr"))

    tr.forEach(function (row) {
        if (!(row.id === "thead")) {
            row.style.display = "none"
        }
    })

    if (filter === "") {
        // If the search input is empty, show all rows
        displayedRows = tr.slice(1) // Exclude the header row
    } else {
        // Filter rows based on the search input
        displayedRows = tr.slice(1).filter(function (row) {
            var cells = Array.from(row.getElementsByTagName("td"))
            return cells.some(function (cell) {
                txtValue = (cell.textContent).toUpperCase() || (cell.innerText).toUpperCase()
                return txtValue.toUpperCase().indexOf(filter) > -1
            })
        })
    }

    // Reset pagination
    setupPagination()
    showPage(1)
}



function setupPagination() {
    var numPages = Math.ceil(displayedRows.length / numPerPage)

    var buttonBack = document.getElementById("pageBack")
    var newButtonBack = buttonBack.cloneNode(true)

    // Remove previous click event listener
    buttonBack.removeEventListener("click", handlePageBackClick)

    buttonBack.parentNode.replaceChild(newButtonBack, buttonBack)

    newButtonBack.addEventListener("click", handlePageBackClick)

    var buttonNext = document.getElementById("pageNext")
    var newButtonNext = buttonNext.cloneNode(true)

    // Remove previous click event listener
    buttonNext.removeEventListener("click", handlePageNextClick)

    buttonNext.parentNode.replaceChild(newButtonNext, buttonNext)

    newButtonNext.addEventListener("click", handlePageNextClick)
}

// Event handler functions
function handlePageBackClick() {
    if ((currentPage - 1) > 0) {
        currentPage -= 1
        showPage(currentPage)
    }
}

function handlePageNextClick() {
    var numPages = Math.ceil(displayedRows.length / numPerPage)
    if ((currentPage + 1) <= numPages) {
        currentPage += 1
        showPage(currentPage)
    }
}


function showPage(pageNum) {
    var numPages = Math.ceil(displayedRows.length / numPerPage)
    document.getElementById("pageIndicator").innerText = pageNum + " z " + numPages

    var start = (pageNum - 1) * numPerPage
    var end = Math.min(start + numPerPage, displayedRows.length)

    // Hide all rows
    displayedRows.forEach(function (row) {
        if (!(row.id === "thead")) {
            row.style.display = "none"
        }
    })

    // Display rows for the current page
    for (var j = start; j < end; j++) {
        displayedRows[j].style.display = ""
    }
}
