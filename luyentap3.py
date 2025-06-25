print('===Vượt qua nỗi sợ===')

name = input('Nhập tên của bạn')
print(f'xin chào{name}! Bạn sắp dấn thân vào hành trình đầy thử thách!')
print('\nChọn kỹ năng đầu của bạn :')
print('1. Dũng cãm')
print('2. Trí tuệ')
print('3. Kiên trì')
choice = input('Chọn 1 trong 3')

if choice == '1':
    skill = 'Dũng cảm'
elif choice == '2':
    skill = 'Trí tuệ'
elif choice == '3':
    skill = 'Kiên trì'
else:
    skill = 'Không xác định'

print(f'\n{name}, kỹ năng{skill}')
print('Cuộc hành trình bắt đầu từ đây!')