.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl
    :alt: License: AGPL-3

======================
Sync Sale Picking Cost
======================

This module allows to synzhronize the cost of sale order lines depending on the outgoing pickings. The cost is updated when the outgoing picking is validated, according to the selected serial number or lot in case the product uses this tracking system, if the stock_valuation_fifo_lot module is installed.


Installation
============

To install this module, you need to:

#. Only install

NOTE. There is a soft dependency on stock_valuation_fifo_lot module, as Odoo uses a financial FIFO valuation, not a real FIFO valuation, which is solved by the stock_valuation_fifo_lot module.


Configuration
=============

To configure this module, you need to:

#. No configuration instructions needed.


Usage
=====

To use this module, you need to:

#. No usage instructions needed.


ROADMAP
=======

[ Enumerate known caveats and future potential improvements.
  It is mostly intended for end-users, and can also help
  potential new contributors discovering new features to implement. ]


Bug Tracker
===========

Bugs and errors are managed in `issues of GitHub <https://github.com/sygel-technology/sy-sale_workflow/issues>`_.
In case of problems, please check if your problem has already been
reported. If you are the first to discover it, help us solving it by indicating
a detailed description `here <https://github.com/sygel-technology/sy-sale_workflow/issues/new>`_.

Do not contact contributors directly about support or help with technical issues.


Credits
=======

Authors
~~~~~~~

* Sygel, Odoo Community Association (OCA)


Contributors
~~~~~~~~~~~~

* Manuel Regidor <manuel.regidor@sygel.es>


Maintainer
~~~~~~~~~~

This module is maintained by Sygel.

.. image:: https://pbs.twimg.com/profile_images/702799639855157248/ujffk9GL_200x200.png
   :alt: Sygel
   :target: https://www.sygel.es

This module is part of the `Sygel/sy-sale_workflow <https://github.com/sygel-technology/sy-sale_workflow>`_.

To contribute to this module, please visit https://github.com/sygel-tecnology.
