function myFunction(p2) 
{
  // console.log(typeof p2);

  const ctx = document.getElementById('myChart')
  
  // const data = 
  // {
  //   labels: JSON.parse(x),
  //   datasets: JSON.parse(p2)
  // };

  const df = 
    {
      datasets:JSON.parse(p2)
    };

  const config = {type: 'line',data: df};
  
  new Chart(ctx, config);

}