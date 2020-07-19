var generated_numbers = []
const ADDRESS = "http://127.0.0.1:5000/"
const STATUS = 'status'

function update_in_table(random_number) {
    table_id = document.getElementById("my_table")
    row = Math.floor(random_number / 10)
    column = (random_number % 10) - 1
    if (random_number % 10 == 0) {
        row -= 1
        column = 9
    }
    document.getElementById("my_table").rows[row].cells[column].innerHTML = random_number
}

function generate_random_number() {
    if (generated_numbers.length == 90) {
        alert('All Done...')
        return
    }
    while (true) {
        var random_number = Math.floor((Math.random() * 90) + 1)
        if (!(generated_numbers.includes(random_number))) {
            break
        }
    }
    console.log('Generated : ', random_number)
    document.getElementById('generated_number').innerHTML = random_number
    update_in_table(random_number)
    generated_numbers.push(random_number)
}

function generate_ticket_callback(data_recv) {
    console.log('Data Received : ', data_recv)
    if (data_recv[STATUS] == true) {
        msg = 'Tickets Saved as : ' + data_recv['ticket_file_name']
    } else {
        msg = 'Tickets could not be generated. See Server Logs...!!!'
    }
    document.getElementById('ticket_result_msg').innerHTML = msg
}

function generate_tickets() {
    var result;
    if (document.getElementById('radio1').checked) {
        result = document.getElementById('ticket_count').value
        console.log('TC : ', result)
    } else if (document.getElementById('radio2').checked) {
        result = document.getElementById('ticket_names').value
        console.log('TN : ', result)
    }

    console.log('Sending Request to Generate Tickets...')
    make_POST('generate_tickets', result, generate_ticket_callback)
}

function check_input_format() {
    document.getElementById('ticket_result_msg').innerHTML = ""
    $("#btn_generate_tickets").prop('disabled', false)
    $("#ticket_count").tooltip('dispose')
    if (document.getElementById('radio1').checked) {
        ticket_count = document.getElementById('ticket_count').value
        if (Number(ticket_count) > 200) {
            $("#btn_generate_tickets").prop('disabled', true)
            $("#ticket_count").tooltip('show')
        }
    } else if (document.getElementById('radio2').checked) {
        ticket_names = document.getElementById('ticket_names').value
        console.log("TN : ", ticket_names)
        if (ticket_names == "") {
            $("#btn_generate_tickets").prop('disabled', true)
        }
    }
}

function make_GET(req, callback) {
    fetch(ADDRESS.concat(req))
        .then(response => response.json())
        .then(data => {
            callback(data)
        })
        .catch(error => console.error(error))
}

function make_POST(req, parameters, callback) {
    fetch(ADDRESS.concat(req), {
            method: 'POST',
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(parameters)
        })
        .then(response => response.json())
        .then(data => {
            callback(data)
        })
        .catch(error => console.error(error))
}