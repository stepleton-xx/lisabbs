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

Very early release. Plenty of bugs. Transfer one file at a time only. Developed
in version 1.0 of the Lisa Pascal Workshop; compatibility with later releases
is unknown.

## Installation

* Copy `TEXT` files to an installation of the Lisa Pascal Workshop, but give
  them all the prefix `XFER/`. Thus, `LIBSORT.TEXT` becomes `XFER/LIBSORT.TEXT`.
* At the Workshop command prompt, type `R <XFER/LisaBBS()i`. The newly compiled
  binary is named `XFER/LisaBBS_exe.Obj`.

## Usage

* Connect another computer to the Lisa via a null modem cable attached to
  Port A. Hardware handshaking (DSR/DTR) is required; for specific cable
  pinouts, refer to Appendix B of the
  [_Basic Lisa Utility_ manual](http://sigmasevensystems.com/blumanual.html).
* Configure the "remote" computer's terminal program for 9600 BPS, 8N1,
  hardware handshaking, no software handshaking.
* To start LisaBBS, at the Workshop command prompt, type `R XFER/LisaBBS_exe`.
* The interface shown above appears simultaneously on the Lisa display and
  on your terminal. Press SPACE or N(ext) to cycle through the directory
  listing. Press T to tag or un-tag individual files, and S to transmit tagged
  files from the Lisa using YMODEM. (_NOTE: At the moment, multi-file send seems
  buggy---you'll have to tag and send files one at a time. But the bug could
  be in my terminal program's YMODEM, who knows._)

Downloaded files are not the "raw" file bytes on disk---instead, they are
tar archives created on the fly with three files inside:

* an `info` file, a text file containing basic Lisa filesystem file metadata
  (modification times and so forth). This information is derived from the
  `Fs_Info` structure returned by Lisa OS's `INFO` system call (think `struct
  stat` on Unix).
* a `label` file, containing the 128-byte user- or program-provided "label" data
  associated with the file.
* a `data` file, holding all of the data within the file itself.

These archives are sometimes called "Lisa Archives" or "lar" files in the code.
The Python program `lartool.py` provides a handy command-line interface for
accessing these file parts. For Lisa-format text files (which are not like
text files as we know them today), `lartool.py` can convert the information
in the archive to ordinary text data.

## Caveats

* Multi-file YMODEM doesn't work. Tag only one file at a time, and don't even
  bother with "send All".
* Some YMODEM bugs may require some packets to be resent, but so far all files
  seem to come through just fine.
* Protected files (e.g. `Pascal.obj`) can't be sent, because the files
  themselves can't be opened (the OS won't let you do that).
* No idea what happens when you try and send a named pipe. Probably something
  gross. Not eager to try.
* LisaBBS will not tell you what items in its file listings are protected or
  named pipes.
* The code that changes the working directory has a bug in its input routine.
  You probably won't be able to change directories.

## Potentially useful elsewhere

`LIBPORT.TEXT` is a handy library for configuring and opening the Lisa serial
port.

`LIBSORT.TEXT` is a generic Quicksort implementation in Pascal.
