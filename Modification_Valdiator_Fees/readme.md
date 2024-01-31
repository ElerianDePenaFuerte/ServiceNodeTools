In default, the servicenode adds the Validator Fee on top of the servicenode fee. In order to leave it to the node operatiors to choose if they like to add the fee on top or just deduct the fee from their proposed fee, this modification was designed.

1. Extend the plugins: in pantos-service-node.conf deduct_validator_fee:

```
plugins:
    bids:
        class: pantos.servicenode.plugins.bids.ConfigFileBidPlugin
        arguments:
            file_path: /etc/pantos-offchain-bids.yaml
        deduct_validator_fee: true
```


deduct_validator_fee: true  = validator Fees are deducted from Node Fees
deduct_validator_fee: false = validator Fees are added on top of Node Fees
