# Using mitmproxy 

## Testing

Record data collection like this

```
mitmdump -s modify_response.py --save-stream-file ./saved_traffic.mitm
```

and I can review it easily like this

```
mitmproxy -r saved_traffic.mitm
```
