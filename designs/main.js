$(document).ready(function(){
    var endpoint = "cause"
    var data ="{{context}}"
    var x = parseInt("{{x}}")
    var y = parseInt("{{y}}")
    var z = parseInt("{{z}}")
    var b = parseInt("{{b}}")
    var c = parseInt("{{c}}")
    console.log(data)
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Accident', 'Unidentified', 'Act of nature', 'Attack', 'Pre-existing conditions'],
            datasets: [{
                label: 'categories of emergency cases',
                data: [x,y,z,b,c],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

  })

  $(document).ready(function(){
    var parklands = parseInt('{{parklands}}')
    var westlands = parseInt('{{westlands}}')
    var spring = parseInt('{{spring}}')
    var riverside = parseInt('{{riverside}}')
    var kile = parseInt('{{kile}}')
    var kilimani = parseInt('{{kilimani}}')
    var loresho = parseInt('{{loresho}}')
    var muthaiga = parseInt('{{muthaig}}')
    var mathare = parseInt('{{mathare}}')
    var mathareN = parseInt('{{mathareN}}')
    var huruma = parseInt('{{huruma}}')
    var kariobangi = parseInt('{{kariobangi}}')
    var shauri = parseInt('{{shauri}}')
    var jericho = parseInt('{{jericho}}')
    var makadara = parseInt('{{makadara}}')
    var doni = parseInt('{{doni}}')
    var uhuru = parseInt('{{uhuru}}')
    var buru = parseInt('{{buru}}')
    var umoja = parseInt('{{umoja}}')
    var ctx = document.getElementById('pickup').getContext('2d');
    var age = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['parklands', 'westlands', 'spring', 'riverside', 'kile', 'kilimani', 'loresho', 'muthaiga', 'mathare', 'huruma', 'kariobangi', 'shauri', 'jericho', 'makadara', 'doni', 'uhuru', 'buru', 'umoja'],
            datasets: [{
                label: '',
                data: [parklands, westlands, spring, riverside, kile, kilimani, loresho, muthaiga, mathare, huruma, kariobangi, shauri, jericho, makadara, doni, uhuru, buru, umoja],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

  })
 
        