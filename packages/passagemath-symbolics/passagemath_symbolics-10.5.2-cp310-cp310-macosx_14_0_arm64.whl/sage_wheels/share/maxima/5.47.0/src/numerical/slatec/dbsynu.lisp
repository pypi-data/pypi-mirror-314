;;; Compiled by f2cl version:
;;; ("f2cl1.l,v 46c1f6a93b0d 2012/05/03 04:40:28 toy $"
;;;  "f2cl2.l,v 96616d88fb7e 2008/02/22 22:19:34 rtoy $"
;;;  "f2cl3.l,v 96616d88fb7e 2008/02/22 22:19:34 rtoy $"
;;;  "f2cl4.l,v 96616d88fb7e 2008/02/22 22:19:34 rtoy $"
;;;  "f2cl5.l,v 46c1f6a93b0d 2012/05/03 04:40:28 toy $"
;;;  "f2cl6.l,v 1d5cbacbb977 2008/08/24 00:56:27 rtoy $"
;;;  "macros.l,v fceac530ef0c 2011/11/26 04:02:26 toy $")

;;; Using Lisp CMU Common Lisp snapshot-2012-04 (20C Unicode)
;;; 
;;; Options: ((:prune-labels nil) (:auto-save t) (:relaxed-array-decls t)
;;;           (:coerce-assigns :as-needed) (:array-type ':simple-array)
;;;           (:array-slicing nil) (:declare-common nil)
;;;           (:float-format double-float))

(in-package :slatec)


(let ((x1 3.0)
      (x2 20.0)
      (pi$ 3.14159265358979)
      (rthpi 0.797884560802865)
      (hpi 1.5707963267949)
      (cc
       (make-array 8
                   :element-type 'double-float
                   :initial-contents '(0.577215664901533 -0.0420026350340952
                                       -0.0421977345555443 0.007218943246663
                                       -2.152416741149e-4 -2.01348547807e-5
                                       1.133027232e-6 6.116095e-9))))
  (declare (type (double-float) x1 x2 pi$ rthpi hpi)
           (type (simple-array double-float (8)) cc))
  (defun dbsynu (x fnu n y)
    (declare (type (simple-array double-float (*)) y)
             (type (f2cl-lib:integer4) n)
             (type (double-float) fnu x))
    (prog ((a (make-array 120 :element-type 'double-float))
           (rb (make-array 120 :element-type 'double-float))
           (cb (make-array 120 :element-type 'double-float)) (ak 0.0) (arg 0.0)
           (a1 0.0) (a2 0.0) (bk 0.0) (cbk 0.0) (cck 0.0) (ck 0.0) (coef 0.0)
           (cpt 0.0) (cp1 0.0) (cp2 0.0) (cs 0.0) (cs1 0.0) (cs2 0.0) (cx 0.0)
           (dnu 0.0) (dnu2 0.0) (etest 0.0) (etx 0.0) (f 0.0) (fc 0.0)
           (fhs 0.0) (fk 0.0) (fks 0.0) (flrx 0.0) (fmu 0.0) (fn 0.0) (fx 0.0)
           (g 0.0) (g1 0.0) (g2 0.0) (p 0.0) (pt 0.0) (q 0.0) (rbk 0.0)
           (rck 0.0) (relb 0.0) (rpt 0.0) (rp1 0.0) (rp2 0.0) (rs 0.0)
           (rs1 0.0) (rs2 0.0) (rx 0.0) (s 0.0) (sa 0.0) (sb 0.0) (smu 0.0)
           (ss 0.0) (st 0.0) (s1 0.0) (s2 0.0) (tb 0.0) (tm 0.0) (tol 0.0)
           (t1 0.0) (t2 0.0) (i 0) (inu 0) (j 0) (k 0) (kk 0) (nn 0))
      (declare (type (f2cl-lib:integer4) nn kk k j inu i)
               (type (double-float) t2 t1 tol tm tb s2 s1 st ss smu sb sa s rx
                                    rs2 rs1 rs rp2 rp1 rpt relb rck rbk q pt p
                                    g2 g1 g fx fn fmu flrx fks fk fhs fc f etx
                                    etest dnu2 dnu cx cs2 cs1 cs cp2 cp1 cpt
                                    coef ck cck cbk bk a2 a1 arg ak)
               (type (simple-array double-float (120)) rb cb a))
      (setf ak (f2cl-lib:d1mach 3))
      (setf tol (max ak 1.0e-15))
      (if (<= x 0.0) (go label270))
      (if (< fnu 0.0) (go label280))
      (if (< n 1) (go label290))
      (setf rx (/ 2.0 x))
      (setf inu (f2cl-lib:int (+ fnu 0.5)))
      (setf dnu (- fnu inu))
      (if (= (abs dnu) 0.5) (go label260))
      (setf dnu2 0.0)
      (if (< (abs dnu) tol) (go label10))
      (setf dnu2 (* dnu dnu))
     label10
      (if (> x x1) (go label120))
      (setf a1 (- 1.0 dnu))
      (setf a2 (+ 1.0 dnu))
      (setf t1 (/ 1.0 (dgamma a1)))
      (setf t2 (/ 1.0 (dgamma a2)))
      (if (> (abs dnu) 0.1) (go label40))
      (setf s (f2cl-lib:fref cc (1) ((1 8))))
      (setf ak 1.0)
      (f2cl-lib:fdo (k 2 (f2cl-lib:int-add k 1))
                    ((> k 8) nil)
        (tagbody
          (setf ak (* ak dnu2))
          (setf tm (* (f2cl-lib:fref cc (k) ((1 8))) ak))
          (setf s (+ s tm))
          (if (< (abs tm) tol) (go label30))
         label20))
     label30
      (setf g1 (- (+ s s)))
      (go label50)
     label40
      (setf g1 (/ (- t1 t2) dnu))
     label50
      (setf g2 (+ t1 t2))
      (setf smu 1.0)
      (setf fc (/ 1.0 pi$))
      (setf flrx (f2cl-lib:flog rx))
      (setf fmu (* dnu flrx))
      (setf tm 0.0)
      (if (= dnu 0.0) (go label60))
      (setf tm (/ (sin (* dnu hpi)) dnu))
      (setf tm (* (+ dnu dnu) tm tm))
      (setf fc (/ dnu (sin (* dnu pi$))))
      (if (/= fmu 0.0) (setf smu (/ (sinh fmu) fmu)))
     label60
      (setf f (* fc (+ (* g1 (cosh fmu)) (* g2 flrx smu))))
      (setf fx (exp fmu))
      (setf p (* fc t1 fx))
      (setf q (/ (* fc t2) fx))
      (setf g (+ f (* tm q)))
      (setf ak 1.0)
      (setf ck 1.0)
      (setf bk 1.0)
      (setf s1 g)
      (setf s2 p)
      (if (or (> inu 0) (> n 1)) (go label90))
      (if (< x tol) (go label80))
      (setf cx (* x x 0.25))
     label70
      (setf f (/ (+ (* ak f) p q) (- bk dnu2)))
      (setf p (/ p (- ak dnu)))
      (setf q (/ q (+ ak dnu)))
      (setf g (+ f (* tm q)))
      (setf ck (/ (* (- ck) cx) ak))
      (setf t1 (* ck g))
      (setf s1 (+ s1 t1))
      (setf bk (+ bk ak ak 1.0))
      (setf ak (+ ak 1.0))
      (setf s (/ (abs t1) (+ 1.0 (abs s1))))
      (if (> s tol) (go label70))
     label80
      (setf (f2cl-lib:fref y (1) ((1 *))) (- s1))
      (go end_label)
     label90
      (if (< x tol) (go label110))
      (setf cx (* x x 0.25))
     label100
      (setf f (/ (+ (* ak f) p q) (- bk dnu2)))
      (setf p (/ p (- ak dnu)))
      (setf q (/ q (+ ak dnu)))
      (setf g (+ f (* tm q)))
      (setf ck (/ (* (- ck) cx) ak))
      (setf t1 (* ck g))
      (setf s1 (+ s1 t1))
      (setf t2 (* ck (- p (* ak g))))
      (setf s2 (+ s2 t2))
      (setf bk (+ bk ak ak 1.0))
      (setf ak (+ ak 1.0))
      (setf s (+ (/ (abs t1) (+ 1.0 (abs s1))) (/ (abs t2) (+ 1.0 (abs s2)))))
      (if (> s tol) (go label100))
     label110
      (setf s2 (* (- s2) rx))
      (setf s1 (- s1))
      (go label160)
     label120
      (setf coef (/ rthpi (f2cl-lib:fsqrt x)))
      (if (> x x2) (go label210))
      (setf etest (/ (cos (* pi$ dnu)) (* pi$ x tol)))
      (setf fks 1.0)
      (setf fhs 0.25)
      (setf fk 0.0)
      (setf rck 2.0)
      (setf cck (+ x x))
      (setf rp1 0.0)
      (setf cp1 0.0)
      (setf rp2 1.0)
      (setf cp2 0.0)
      (setf k 0)
     label130
      (setf k (f2cl-lib:int-add k 1))
      (setf fk (+ fk 1.0))
      (setf ak (/ (- fhs dnu2) (+ fks fk)))
      (setf pt (+ fk 1.0))
      (setf rbk (/ rck pt))
      (setf cbk (/ cck pt))
      (setf rpt rp2)
      (setf cpt cp2)
      (setf rp2 (- (* rbk rpt) (* cbk cpt) (* ak rp1)))
      (setf cp2 (- (+ (* cbk rpt) (* rbk cpt)) (* ak cp1)))
      (setf rp1 rpt)
      (setf cp1 cpt)
      (setf (f2cl-lib:fref rb (k) ((1 120))) rbk)
      (setf (f2cl-lib:fref cb (k) ((1 120))) cbk)
      (setf (f2cl-lib:fref a (k) ((1 120))) ak)
      (setf rck (+ rck 2.0))
      (setf fks (+ fks fk fk 1.0))
      (setf fhs (+ fhs fk fk))
      (setf pt (max (abs rp1) (abs cp1)))
      (setf fc (+ (expt (/ rp1 pt) 2) (expt (/ cp1 pt) 2)))
      (setf pt (* pt (f2cl-lib:fsqrt fc) fk))
      (if (> etest pt) (go label130))
      (setf kk k)
      (setf rs 1.0)
      (setf cs 0.0)
      (setf rp1 0.0)
      (setf cp1 0.0)
      (setf rp2 1.0)
      (setf cp2 0.0)
      (f2cl-lib:fdo (i 1 (f2cl-lib:int-add i 1))
                    ((> i k) nil)
        (tagbody
          (setf rpt rp2)
          (setf cpt cp2)
          (setf rp2
                  (/
                   (- (* (f2cl-lib:fref rb (kk) ((1 120))) rpt)
                      (* (f2cl-lib:fref cb (kk) ((1 120))) cpt)
                      rp1)
                   (f2cl-lib:fref a (kk) ((1 120)))))
          (setf cp2
                  (/
                   (-
                    (+ (* (f2cl-lib:fref cb (kk) ((1 120))) rpt)
                       (* (f2cl-lib:fref rb (kk) ((1 120))) cpt))
                    cp1)
                   (f2cl-lib:fref a (kk) ((1 120)))))
          (setf rp1 rpt)
          (setf cp1 cpt)
          (setf rs (+ rs rp2))
          (setf cs (+ cs cp2))
          (setf kk (f2cl-lib:int-sub kk 1))
         label140))
      (setf pt (max (abs rs) (abs cs)))
      (setf fc (+ (expt (/ rs pt) 2) (expt (/ cs pt) 2)))
      (setf pt (* pt (f2cl-lib:fsqrt fc)))
      (setf rs1 (/ (+ (* rp2 (/ rs pt)) (* cp2 (/ cs pt))) pt))
      (setf cs1 (/ (- (* cp2 (/ rs pt)) (* rp2 (/ cs pt))) pt))
      (setf fc (- (* hpi (- dnu 0.5)) x))
      (setf p (cos fc))
      (setf q (sin fc))
      (setf s1 (* (- (* cs1 q) (* rs1 p)) coef))
      (if (or (> inu 0) (> n 1)) (go label150))
      (setf (f2cl-lib:fref y (1) ((1 *))) s1)
      (go end_label)
     label150
      (setf pt (max (abs rp2) (abs cp2)))
      (setf fc (+ (expt (/ rp2 pt) 2) (expt (/ cp2 pt) 2)))
      (setf pt (* pt (f2cl-lib:fsqrt fc)))
      (setf rpt
              (+ dnu 0.5 (/ (- (+ (* rp1 (/ rp2 pt)) (* cp1 (/ cp2 pt)))) pt)))
      (setf cpt (+ x (/ (- (+ (* cp1 (/ rp2 pt)) (* -1 rp1 (/ cp2 pt)))) pt)))
      (setf cs2 (- (* cs1 cpt) (* rs1 rpt)))
      (setf rs2 (+ (* rpt cs1) (* rs1 cpt)))
      (setf s2 (/ (* (+ (* rs2 q) (* cs2 p)) coef) x))
     label160
      (setf ck (/ (+ dnu dnu 2.0) x))
      (if (= n 1) (setf inu (f2cl-lib:int-sub inu 1)))
      (if (> inu 0) (go label170))
      (if (> n 1) (go label190))
      (setf s1 s2)
      (go label190)
     label170
      (f2cl-lib:fdo (i 1 (f2cl-lib:int-add i 1))
                    ((> i inu) nil)
        (tagbody
          (setf st s2)
          (setf s2 (- (* ck s2) s1))
          (setf s1 st)
          (setf ck (+ ck rx))
         label180))
      (if (= n 1) (setf s1 s2))
     label190
      (setf (f2cl-lib:fref y (1) ((1 *))) s1)
      (if (= n 1) (go end_label))
      (setf (f2cl-lib:fref y (2) ((1 *))) s2)
      (if (= n 2) (go end_label))
      (f2cl-lib:fdo (i 3 (f2cl-lib:int-add i 1))
                    ((> i n) nil)
        (tagbody
          (setf (f2cl-lib:fref y (i) ((1 *)))
                  (- (* ck (f2cl-lib:fref y ((f2cl-lib:int-sub i 1)) ((1 *))))
                     (f2cl-lib:fref y ((f2cl-lib:int-sub i 2)) ((1 *)))))
          (setf ck (+ ck rx))
         label200))
      (go end_label)
     label210
      (setf nn 2)
      (if (and (= inu 0) (= n 1)) (setf nn 1))
      (setf dnu2 (+ dnu dnu))
      (setf fmu 0.0)
      (if (< (abs dnu2) tol) (go label220))
      (setf fmu (* dnu2 dnu2))
     label220
      (setf arg (- x (* hpi (+ dnu 0.5))))
      (setf sa (sin arg))
      (setf sb (cos arg))
      (setf etx (* 8.0 x))
      (f2cl-lib:fdo (k 1 (f2cl-lib:int-add k 1))
                    ((> k nn) nil)
        (tagbody
          (setf s1 s2)
          (setf t2 (/ (- fmu 1.0) etx))
          (setf ss t2)
          (setf relb (* tol (abs t2)))
          (setf t1 etx)
          (setf s 1.0)
          (setf fn 1.0)
          (setf ak 0.0)
          (f2cl-lib:fdo (j 1 (f2cl-lib:int-add j 1))
                        ((> j 13) nil)
            (tagbody
              (setf t1 (+ t1 etx))
              (setf ak (+ ak 8.0))
              (setf fn (+ fn ak))
              (setf t2 (/ (* (- t2) (- fmu fn)) t1))
              (setf s (+ s t2))
              (setf t1 (+ t1 etx))
              (setf ak (+ ak 8.0))
              (setf fn (+ fn ak))
              (setf t2 (/ (* t2 (- fmu fn)) t1))
              (setf ss (+ ss t2))
              (if (<= (abs t2) relb) (go label240))
             label230))
         label240
          (setf s2 (* coef (+ (* s sa) (* ss sb))))
          (setf fmu (+ fmu (* 8.0 dnu) 4.0))
          (setf tb sa)
          (setf sa (- sb))
          (setf sb tb)
         label250))
      (if (> nn 1) (go label160))
      (setf s1 s2)
      (go label190)
     label260
      (setf coef (/ rthpi (f2cl-lib:fsqrt x)))
      (setf s1 (* coef (sin x)))
      (setf s2 (* (- coef) (cos x)))
      (go label160)
     label270
      (xermsg "SLATEC" "DBSYNU" "X NOT GREATER THAN ZERO" 2 1)
      (go end_label)
     label280
      (xermsg "SLATEC" "DBSYNU" "FNU NOT ZERO OR POSITIVE" 2 1)
      (go end_label)
     label290
      (xermsg "SLATEC" "DBSYNU" "N NOT GREATER THAN 0" 2 1)
      (go end_label)
     end_label
      (return (values nil nil nil nil)))))

(in-package #:cl-user)
#+#.(cl:if (cl:find-package '#:f2cl) '(and) '(or))
(eval-when (:load-toplevel :compile-toplevel :execute)
  (setf (gethash 'fortran-to-lisp::dbsynu
                 fortran-to-lisp::*f2cl-function-info*)
          (fortran-to-lisp::make-f2cl-finfo
           :arg-types '((double-float) (double-float)
                        (fortran-to-lisp::integer4)
                        (simple-array double-float (*)))
           :return-values '(nil nil nil nil)
           :calls '(fortran-to-lisp::xermsg fortran-to-lisp::dgamma
                    fortran-to-lisp::d1mach))))

