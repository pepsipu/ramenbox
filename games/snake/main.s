	.org $4000
game_loop:
	; restore cursor to orgional byte
	ldx x_pos
	ldy y_pos
	lda cursor_save
	.byte $ff ; draw pixel with accumulator
	.byte 13
	lda $ee00
	cmp #2
	beq left_stick
	cmp #4
	beq right_stick
	cmp #8
	beq down_stick
	cmp #16
	beq up_stick
	jmp draw_cursor
left_stick:
	lda x_pos
	sbc #5
	sta x_pos
	jmp draw_cursor
right_stick:
	lda x_pos
	adc #5
	sta x_pos
	jmp draw_cursor
up_stick:
	lda y_pos
	sbc #5
	sta y_pos
	jmp draw_cursor
down_stick:
	lda y_pos
	adc #5
	sta y_pos

draw_cursor:
	.byte $ff ; save byte before we overwrite it with cursor
	.byte 16
	sta cursor_save

	ldx x_pos
	ldy y_pos
	.byte $ff ; write 0xff on x and y pos
	.byte 11
	.byte $ff

	.byte $ff ; transfer to display
	.byte 10
	; after this we will restore the byte that the cursor overwrote
	jmp game_loop
x_pos: .byte 10
y_pos: .byte 10
cursor_save: .byte 00
maze:
