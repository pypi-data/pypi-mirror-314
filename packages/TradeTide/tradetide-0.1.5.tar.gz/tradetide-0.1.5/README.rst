|Logo|

|python|
|docs|
|PyPi|
|PyPi_download|

TradeTide
=========

TradeTide is a trading platform designed to empower traders with advanced analytics, real-time market data, and automated trading capabilities. Our platform caters to both novice and experienced traders, offering a wide range of tools to analyze market trends, execute trades, and manage portfolios efficiently.


Testing
*******

To test localy (with cloning the GitHub repository) you'll need to install the dependencies and run the coverage command as

.. code:: python

   >>> git clone https://github.com/MartinPdeS/TradeTide.git
   >>> cd TradeTide
   >>> pip install -r requirements/requirements.txt
   >>> pytest

----


Coding example
**************

.. code-block:: python

   from TradeTide import BackTester, indicators, get_market_data
   from TradeTide import capital_managment, risk_management

   market_data = get_market_data('eur', 'usd', year=2023, time_span='30day', spread=0)

   indicator = indicators.BB(periods=20)

   indicator.generate_signal(market_data)

   indicator.plot()

   backtester = BackTester(market=market_data, strategy=indicator)

   risk = risk_management.DirectLossProfit(
       market=market_data,
       stop_loss='10pip',
       take_profit='10pip',
   )

   capital_managment = capital_managment.LimitedCapital(
       initial_capital=100_000,
       risk_management=risk,
       max_cap_per_trade=10_000,
       limit_of_positions=1,
       micro_lot=1_000
   )

   backtester.backtest(capital_managment=capital_managment)


   backtester.plot(show_price=True)

   metrics = backtester.metrics

   metrics.print()


|example_image|

----


Contact Information
************************
As of 2024, the project is still under development. If you want to collaborate, it would be a pleasure! I encourage you to contact me.

PyMieSim was written by `Martin Poinsinet de Sivry-Houle <https://github.com/MartinPdS>`_  .

Email:`martin.poinsinet-de-sivry@polymtl.ca <mailto:martin.poinsinet-de-sivry@polymtl.ca?subject=TradeTide>`_ .


.. |python| image:: https://img.shields.io/pypi/pyversions/pymiesim.svg
   :target: https://www.python.org/

.. |Logo| image:: https://github.com/MartinPdeS/TradeTide/raw/master/docs/images/logo.png

.. |example_image| image:: https://github.com/MartinPdeS/TradeTide/raw/master/docs/images/image_example.png

.. |docs| image:: https://github.com/martinpdes/tradetide/actions/workflows/deploy_documentation.yml/badge.svg
   :target: https://martinpdes.github.io/TradeTide/
   :alt: Documentation Status

.. |PyPi| image:: https://badge.fury.io/py/TradeTide.svg
    :target: https://badge.fury.io/py/TradeTide

.. |PyPi_download| image:: https://img.shields.io/pypi/dm/TradeTide.svg
    :target: https://pypistats.org/packages/tradetide

.. |coverage| image:: https://raw.githubusercontent.com/MartinPdeS/TradeTide/python-coverage-comment-action-data/badge.svg
   :alt: Unittest coverage
   :target: https://htmlpreview.github.io/?https://github.com/MartinPdeS/TradeTide/blob/python-coverage-comment-action-data/htmlcov/index.html