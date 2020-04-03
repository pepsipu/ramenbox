  .org $4000
load_ptr:
  lda #$fd
  sta $01
  lda #$00
  sta $00
  ldx #$aa
write_buf:
  txa
  sta ($00),Y
  iny
  inx
  cpy #$ff
  bne write_buf
  .byte $ff
  .byte $0a
loop:
  ;jmp loop
