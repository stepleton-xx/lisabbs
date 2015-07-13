# lisabbs

Transfer files off of your Apple Lisa with a null modem cable using your
favorite terminal program (as long as it supports YMODEM file transfers).

## Screenshot

```
{V1.0} BBS: Next, Prev, Online, Chdir, Tag, Send tagged, send All, Misc, ?

 A)  Assembler.obj
 B)  ByteDiff.obj
 C)  Changeseg.obj
 D)  Code.obj
 E)  Codesize.obj
 F)  Diff.obj
 G)  Dumpobj.obj
 H)  DumpPatch.obj
 I)  EDIT.MENUS.TEXT
 J)  Editor.obj
 K)  Filediv.obj
 L)  Filejoin.obj
 M)  find.obj
 N)  FMDATA
 O)  font.heur
 P)  font.lib
 Q)  Gxref.obj
 R)  Intrinsic.lib
 S)  IOSFplib.obj
 T)  IOSPaslib.obj

Page 1 of -SLOT2CHAN1, 0 tagged
```

## Status

Early release. Plenty of bugs. Transfer one file at a time only. Developed in
version 1.0 of the Lisa Pascal Workshop; compatibility with later releases
is unknown.

## Installation

* Copy `TEXT` files to an installation of the Lisa Pascal Workshop, but give
  them all the prefix `XFER/`. Thus, `LIBSORT.TEXT` becomes `XFER/LIBSORT.TEXT`.
* At the Workshop command prompt, type `R<XFER/LisaBBS()i`. The newly compiled
  binary is named `XFER/LisaBBS_exe.Obj`.

## Usage

* Connect another computer to the Lisa via a null modem cable attached to
  Port A. Hardware handshaking (DSR/DTR) is required; for specific cable
  pinouts, refer to Appendix B of the
  [_Basic Lisa Utility_ manual](http://sigmasevensystems.com/blumanual.html).
* Configure the "remote" computer's terminal program for 9600 BPS, 8N1,
  hardware handshaking, no software handshaking.
* To start LisaBBS, at the Workshop command prompt, type `RXFER/LisaBBS_exe`.
