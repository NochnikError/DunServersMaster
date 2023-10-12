┌────────────┬─────────┐
│ Device:    │ C:\\     │
│ Total:     │ 166.0G  │
│ Used:      │ 92.2G   │
│ Free:      │ 73.8G   │
│ Use:       │    55%  │
│ Type:      │ NTFS    │
│ Mount:     │ C:\\     │
└────────────┴─────────┘
┌────────────┬─────────┐
│ Device:    │ C:\     │
│ Total:     │ 166.0G  │
│ Used:      │ 92.2G   │
│ Free:      │ 73.8G   │
│ Use:       │    55%  │
│ Type:      │ NTFS    │
│ Mount:     │ C:\     │
└────────────┴─────────┘
---------
┌────────────┬─────────┐
│ Device:    │ D:\     │
│ Total:     │ 14.4G   │
│ Used:      │ 4.4G    │
│ Free:      │ 10.1G   │
│ Use:       │    30%  │
│ Type:      │ NTFS    │
│ Mount:     │ D:\     │
└────────────┴─────────┘
'
#
#
# def on_terminate(proc):
#     print(f"Процесс {proc} завершается с кодом {proc.returncode}")
#
#
# procs = psutil.Process().children()
# for p in procs:
#     p.terminate()
# gone, alive = psutil.wait_procs(procs, timeout=3, callback=on_terminate)
# for p in alive:
#     p.kill()
