function myFunction(x,p2) 
{
  console.log(typeof p2);

  const ctx = document.getElementById('myChart');

  const data = 
  {
    labels: JSON.parse(x),
    datasets: JSON.parse(p2)
  };

  const config = {type: 'line',data: data};
  new Chart(ctx, config);
}