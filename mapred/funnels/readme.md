input: openplay clickstream logs (web clickstream will fall on looking for "properties" object) 

example: 
```
grep '"app": "openplay"' example.log | 
grep -E "app_opened|track_playback_delay" | 
bash run_funnel.sh 'app_opened track_playback_delay'
```