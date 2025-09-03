ollama serve &

pid=$!

sleep 5
echo "Retrieve model..."
ollama pull deepseek-r1:7b
echo "Done."
wait $pid