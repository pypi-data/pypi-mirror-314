# Hindi POS tagger 

### Hindi POS tagger developed by Dr. Nisheeth Joshi at SLP Lab, Centre for Artificial Intelligence, Banasthali Vidyapith.

## Installation:
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install hindiPOS
```bash
pip install hindiPOS
```

## Usage
```python
from hindiPOS import hmm
#returns a list
hmm.postag('दिल्ली भारत की राजधानी है।')
#['दिल्ली|NNP', 'भारत|NNP', 'की|PSP', 'राजधानी|NN', 'है।|NN']
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)