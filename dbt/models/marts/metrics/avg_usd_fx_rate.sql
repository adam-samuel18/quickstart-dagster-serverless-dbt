select * 
from {{ metrics.calculate(
    metric('avg_usd_fx_rate'),
    grain='week'
) }}