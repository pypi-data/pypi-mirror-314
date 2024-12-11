Changelog
=========


2.0.0 (2024-12-11)
------------------

- BIBLI-73 : Update to Plone6 (6.0.9)
  [boulch]

- BIBLI-73 : Change default faceted view for "explorer" folders
  [boulch]

- Migrate to Plone 6. Next steps!
  [boulch]

- Migration to Plone6
  [boulch]


1.1.17 (2024-02-16)
-------------------

- WEB-4074 : Install collective.plausible
  [remdub]


1.1.16 (2023-08-23)
-------------------

- clear configure_faceted (in upgrades.py). Manually done on each instance due to missing taxonomies
  [boulch]


1.1.15 (2023-08-09)
-------------------

- MBIBLIWLHA-6 : Change value of Plone.thumb_scale_listing to display bigger picture in library folders views
  [boulch]


1.1.14 (2023-07-05)
-------------------

- Migration to Plone6
- Create upgrade step to reimport faceted "explorer" config (Fix select2 widgets)


1.1.17 (2024-02-16)
-------------------

- WEB-4074 : Install collective.plausible
  [remdub]


1.1.16 (2023-08-23)
-------------------

- clear configure_faceted (in upgrades.py). Manually done on each instance due to missing taxonomies
  [boulch]


1.1.15 (2023-08-09)
-------------------

- MBIBLIWLHA-6 : Change value of Plone.thumb_scale_listing to display bigger picture in library folders views
  [boulch]


1.1.14 (2023-07-05)
-------------------

- Create upgrade step to reimport faceted "explorer" config (Fix select2 widgets)
  [boulch]


1.1.13 (2022-02-28)
-------------------

- Add collective.big.bang dependency
  [boulch]


1.1.12 (2021-02-05)
-------------------

- Correct issue when upload 1.1.11 on pypi.
  [boulch]


1.1.11 (2021-02-04)
-------------------

- Add iaweb.mosaic as a requirement (to add slider in bibliotheca).
  [boulch]


1.1.10 (2020-09-30)
-------------------

- [BIBLI-46] : Set content language same as DefaultLanguage site (upgrade step).
  [boulch]


1.1.9 (2020-09-14)
------------------

- BIBLI-41: Add translations for show/hide button on faceted view
  [mpeeters]


1.1.8 (2020-09-14)
------------------

- Use default config coordinates when there is no marker to display on faceted map
  [mpeeters]

- BIBLI-29: Fix a javascript error when there is no geolocated result to display for faceted map
  [mpeeters]

- BIBLI-41: Fix show/hide button for faceted map
  [mpeeters]


1.1.7 (2020-09-03)
------------------

- [BIBLI-39] : Add image cropping and banner behaviors on Folder and Document types.
  [boulch]


1.1.6 (2020-09-02)
------------------

- [BIBLI-38] : Load @@images/image/mini instead of @@images/image in explorer faceted view.
  [boulch]

1.1.5 (2020-08-20)
------------------

- [BIBLI-25] : Fix pppw items index in explorer template.
  [boulch]


1.1.4 (2020-08-19)
------------------

- [BIBLI-25] : Refactor explorer template to fix a bug when loading map.
  [boulch]


1.1.3 (2020-08-13)
------------------

- [BIBLI-12] : Directly apply custom faceted view on "explorer" folder.
  [boulch]
- [BIBLI-12] : Register custom faceted "map" template
  [boulch]


1.1.2 (2020-07-24)
------------------

- Add new package : collective.faceted.map. To geolocalize "patrimoine" type.
  [boulch]


1.1.1 (2020-03-12)
------------------

- Set recaptcha as default captcha settings on plone.app.discussion.
  [bsuttor]

- Install plone.formwidget.recaptcha during policy installation.
  [bsuttor]


1.1.0 (2020-03-11)
------------------

- Add plone.formwidget.recaptcha dependency.
  [bsuttor]


1.0a6 (2019-01-07)
------------------

- Add collective.cookiecuttr dependency.
  [bsuttor]


1.0a5 (2018-09-04)
------------------

- Add collective.z3cform.select2
  [daggelpop]


1.0a4 (2018-08-06)
------------------

- Fix ZCML imports
  [vpiret]


1.0a3 (2018-07-27)
------------------

- Add library.core
  [daggelpop]

- Add collective.preventactions
  [daggelpop]


1.0a2 (2018-07-10)
------------------

- Add collective.easyform
  [daggelpop]

- Add collective.behavior.banner
  [daggelpop]

- Add collective.behavior.gallery
  [daggelpop]


1.0a1 (2018-06-20)
------------------

- Initial release.
  [daggelpop]
