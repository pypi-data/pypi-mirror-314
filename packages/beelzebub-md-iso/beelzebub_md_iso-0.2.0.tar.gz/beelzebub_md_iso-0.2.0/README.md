# beelzebub-md-iso

Beelzebub-md-iso is a subpackage of [beelzebub](https://github.com/paul-breen/beelzebub).  Given a metadata record in [mdJSON](https://www.adiwg.org/projects/#mdjson-schemas) format, it will translate it to [ISO19115-2](https://www.iso.org/standard/67039.html) format.

## Example Usage

```
from beelzebub.md_iso import MdjsonToISO19115_2

conf = {
    'reader': {'iotype': 'file'},
    'writer': {'iotype': 'file'}
}
in_file = '/path/to/mdjson/metadata.json'
out_file = '/path/to/iso19115-2/metadata.xml'

x = MdjsonToISO19115_2(conf=conf)
x.run(in_file, out_file)
```

#### References

NOAA have useful [metadata resources](https://www.ncei.noaa.gov/resources/metadata), including this [ISO Workbook](http://www.ncei.noaa.gov/sites/default/files/2020-04/ISO%2019115-2%20Workbook_Part%20II%20Extentions%20for%20imagery%20and%20Gridded%20Data.pdf) and this [collection level metadata template](https://data.noaa.gov/waf/templates/iso_u/xml/ncei_template.xml).

