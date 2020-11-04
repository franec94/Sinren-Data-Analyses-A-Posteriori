@echo on
@cls

python calculate_jpeg_compression.py ^
    --image_files fake.jpeg test001.png lena.jpg ^
    --dirs C:\Users\path\totestsets\BSD68 ^
    --sidelength 256 ^
    --min_quality 92 ^
    --max_quality 95 ^
    --db_resource C:\Users\path\to\compressions-db-train.db
    
:: --show_results_via_table
::  --enable_loggging ^
