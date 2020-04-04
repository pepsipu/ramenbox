	.org $4000
game_loop:
	lda $ee00
	cmp #2
	beq left_stick
	cmp #4
	beq right_stick
	cmp #8
	beq down_stick
	cmp #16
	beq up_stick
	jmp game_loop
left_stick:
	dec x_pos
	jmp game_loop
right_stick:
	inc x_pos
	jmp game_loop
up_stick:
	inc y_pos
	jmp game_loop
down_stick:
	dec y_pos
	jmp game_loop

x_pos: .byte 00
y_pos: .byte 00
