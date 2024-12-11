CC = gcc

CFLAGS = -fPIC -Wall
LDFLAGS = -shared
POSFLAGS = -O -g
OBJFLAGS = -c -o

all: libeuclidean.so libmanhattan.so libeditdist.so liblcss.so libfrechet.so libhausdorff.so libdtw.so librdp.so libsad.so

libeuclidean.so:
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ src/euclidean.c

libfrechet.so:
	$(CC) $(CFLAGS) $(POSFLAGS) src/euclidean.c $(OBJFLAGS) euclidean.pic.o
	$(CC) $(CFLAGS) $(POSFLAGS) src/frechet.c $(OBJFLAGS) frechet.pic.o
	$(CC) $(LDFLAGS) euclidean.pic.o frechet.pic.o -o $@
	rm *.pic.o

libhausdorff.so:
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ src/hausdorff.c
	
libsad.so:
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ src/sad.c

libmanhattan.so:
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ src/manhattan.c

libeditdist.so:
	$(CC) $(CFLAGS) $(POSFLAGS) src/manhattan.c $(OBJFLAGS) manhattan.pic.o
	$(CC) $(CFLAGS) $(POSFLAGS) src/edit_distance.c $(OBJFLAGS) editdist.pic.o
	$(CC) $(LDFLAGS) manhattan.pic.o editdist.pic.o -o $@
	rm *.pic.o

liblcss.so:
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ src/lcss.c

librdp.so:
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ src/rdp.c	

libdtw.so:
	$(CC) $(CFLAGS) $(POSFLAGS) src/trajectory.c $(OBJFLAGS) trajectory.pic.o
	$(CC) $(CFLAGS) $(POSFLAGS) src/matrix.c $(OBJFLAGS) matrix.pic.o
	$(CC) $(CFLAGS) $(POSFLAGS) src/euclidean.c $(OBJFLAGS) euclidean.pic.o
	$(CC) $(CFLAGS) $(POSFLAGS) src/dtw.c $(OBJFLAGS) dtw.pic.o
	$(CC) $(LDFLAGS) trajectory.pic.o matrix.pic.o euclidean.pic.o dtw.pic.o -o $@
	rm *.pic.o

clean:
	rm -f *.so *.o
	[ -e "dist" ] && rm -r dist || :
	[ -e "stmeasures-clib" ] && rm -r stmeasures-clib || :
	pip uninstall -y stmeasures
