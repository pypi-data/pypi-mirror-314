Changelog
=========


2.1.2 (2024-12-12)
------------------

- BIBLI-73 : Fix js for map
  [boulch, tlambert, laulaz]


2.1.1 (2024-12-11)
------------------

- BIBLI-73 : Add monkeypatch to fix TTW resource calling
  [boulch]


2.1.0 (2024-12-11)
------------------

- BIBLI-73 : Update to Plone6 (6.0.9)
  [boulch]


2.0.15 (2023-12-12)
-------------------

- MBIBLIHAVA-3 : Fix "Impossible to add/save existing content tile" (view_template field : required must be False)
  issue : https://github.com/plone/plone.app.standardtiles/issues/149
  [boulch]


2.0.14 (2021-09-16)
-------------------

- Fix previous release
  [boulch]


2.0.13 (2021-09-15)
-------------------

- Add an honeypot field to comment form
  [boulch]


2.0.12 (2020-10-09)
-------------------

- BIBLI-45: Show coordinates for geolocated content
  [mpeeters]

- BIBLI-45: Do not show map when the context is not geolocated
  [mpeeters]
- [MBIBLIMCYA-2] Fix file field and define a file size vaildator.


2.0.11 (2020-09-01)
-------------------

- [BIBLI-35] Get geolocation widget in patrimoine view
  [boulch]


2.0.10 (2020-08-31)
-------------------

- Fix patrimoine template.
  [boulch]


2.0.9 (2020-08-31)
------------------

- Fix some display issues in patrimoine template.
  [boulch]
- Fix a vocabulary bug.
  [boulch]


2.0.8 (2020-08-27)
------------------

- [BIBLI-28] : By default, patrimoine types have 4 taxonomies installed.
  [boulch]

2.0.7 (2020-08-20)
------------------

- [BIBLI-26] : No render of widgets (other than "Bien & PPPW") when no values in field and no render of group/label if no widgets values under this group.
  [boulch]
- [BIBLI-26] : No render of "Bien & PPPW" widgets when no values in field.
  [boulch]

2.0.6 (2020-07-24)
------------------

- Add method to clear pppw titles when there is no field under this title
  [boulch]
- Rename pppw titles (remove digits)
  [boulch]


2.0.5 (2020-07-22)
------------------

- Change some default values to None in PPPW
  [boulch]


2.0.4 (2020-07-22)
------------------

- Add some permissions restrictions to hide "PPPW personal informations Owner" to anonymous user
  [boulch]
- Create vocabularies for "provinces" and "municipalities"
  [boulch]
- Create a TextTitleWidget to divide PPPW in some "section".
  [boulch]
- Change patrimoine xml schema to model schema
  [boulch]


2.0.3 (2020-05-07)
------------------

- Add missing dependency.
  [bsuttor]


2.0.2 (2020-05-07)
------------------

- Fix six.text_typeS > six.text_type [BIBLI-14]
  [boulch]
- Add is_geolocated tests
  [boulch]
- Add is_geolocated indexer
  [boulch]
- Change value to fix how to get LeadImage Behavior (.ILeadImage bug when reinstall library.core
  [boulch]
- Add behavior to patrimoine content: collective.geolocationbehavior.geolocation.IGeolocatable.
  [bsuttor]


2.0.1 (2020-03-13)
------------------

- Fix python3 partimoine content indexing.
  [bsuttor]

- Adding first tests.
  [bsuttor]


2.0.0 (2020-03-11)
------------------

- Breaking change: become Plone 5.2 and python 3 compatible only.
  [bsuttor]


1.0a8 (2018-10-02)
------------------

- Upgrade step to purge Patrimoine lead image scales
  [daggelpop]


1.0a7 (2018-09-28)
------------------

- Enable Full text search on `Patrimoine`
  [daggelpop]

- Scale `Patrimoine` lead image without cropping
  [daggelpop]

- Show caption under `Patrimoine` lead image
  [daggelpop]

- Fix error when there is no categorization
  [daggelpop]


1.0a6 (2018-09-14)
------------------

- Reorder fields in `Patrimoine` view
  [daggelpop]

- Integrate `Patrimoine` lead image with the fancybox gallery
  [daggelpop]

- Add lieu field in `Patrimoine`
  [daggelpop]


1.0a5 (2018-09-04)
------------------

- Extend accepted date encoding formats for `Patrimoine`
  [daggelpop]

- Use collective.z3cform.select2 widgets for taxonomy input
  [daggelpop]


1.0a4 (2018-08-13)
------------------

- Hide contenus_lies in `Patrimoine` when there is none
  [daggelpop]

1.0a3 (2018-08-09)
------------------

- Fix description for `Patrimoine` field
  [vpiret]

1.0a2 (2018-08-08)
------------------

- Fix default value for `informations` field
  [vpiret]

- Add a custom view for `Patrimoine` content type to fix an issue with
  related items
  [vpiret]

- Extend `Patrimoine` to add more fields
  [vpiret]


1.0a1 (2018-07-27)
------------------

- Add content-type Patrimoine
  [daggelpop]

- Initial release.
  [daggelpop]
