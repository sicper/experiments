(ns tiny-scheme.core
  (:gen-class))

;; declare
(declare eval1)
(declare apply1)

;; construct java hash-map
(defn jhash-map
  [& opts]
  (doto (java.util.HashMap.) (.putAll (apply hash-map opts))))

(defn put!
  [^java.util.Map m k v]
  (.put m k v))

(defn remove!
  [^java.util.Map m k]
  (.remove m k))

(defn immutable!
  [m]
  (into {} m))


;; Global Environment
;;  a transient map
(def global-env (jhash-map))

(defn extend-environment
  [params values env]
  (cond
   (not= (count params) (count values)) (throw (Exception. "arguments number unexcepted!"))
   :else (doseq [[p v] (map list params values)]
           (put! env p v))))


;; An example:
;;  (tagged-list? '(function (x) ((+ x 1))) 'function)
;;  => true
(defn tagged-list?
  [expr symbol]
  (and (list? expr)
       (= (first expr) symbol)))

;; built-in combination functions
;; cons, car, cdr
(defn make-pair
  [x y]
  (list 'pair x y))

(def cons-proc make-pair)
(defn car-proc
  [pair]
  (let [[_ x y] (vec pair)]
    x))

(defn cdr-proc
  [pair]
  (let [[_ x y] (vec pair)]
    y))

(def list-proc list)

;; number?: clojure built-in function
;; string?: clojure built-in function
;; list?: clojure built-in function
;; symbol?: clojure built-in function

;; just true or false
(defn bool?
  [expr]
  (or (= expr 'true)
      (= expr 'false)))

;; An example:
;;  '(1 . 2)
;;  '(1 2 3)
(defn pair?
  [expr]
  (or (list? expr)
      (tagged-list? expr 'pair)))


;; variable
;; stored object {:var '(variable value)}
(defn make-variable
  [value]
  (list 'variable value))

(defn get-variable-object
  [var env]
  (get env var))

(defn get-variable-value
  [var env]
  (second (get env var)))

(defn variable?
  [expr]
  (and (symbol? expr)
       (tagged-list?
        (get-variable-object expr global-env)
        'variable)))

;; built-in funtions:
;;  stored object: {:fn-name '(built-in-function procedure)}
;;  contains:
;;    boolean: and, or, not
;;    number: +, -, *, /, >, <, =, mod
;;    pair/list: cons, car, cdr, list, null?
(defn built-in-function?
  [expr]
  (tagged-list?
   expr
   'built-in-function))

(defn make-built-in-function
  [proc]
  (list 'built-in-function proc))

(defn get-built-in-procedure
  [fn-object]
  (second fn-object))

;; user-function
;; stored object: {:fn-name '(function fn-params fn-body)}
(defn make-user-function
  [fn-params fn-body fn-env]
  (list 'function fn-params fn-body fn-env))

(defn get-user-function-object
  [fn-name env]
  (get env fn-name))

(defn get-user-function-params
  [fn-name env]
  (second (get env fn-name)))

(defn get-user-function-body
  [fn-name env]
  (nth (get env fn-name) 2))

(defn get-user-function-env
  [fn-name env]
  (nth (get env fn-name) 3))

(defn user-function?
  [expr]
  (tagged-list?
   (get-user-function-object expr global-env)
   'function))

(defn function?
  [expr]
  (and (symbol? expr)
       (or (built-in-function? expr)
           (user-function? expr))))


;; function-called?
;;  format like '(fn args)
(defn function-called?
  [expr]
  (and (list? expr)
       (let [[fn-name & fn-args] (vec expr)]
         (symbol? fn-name))))


;; user-function-defined?
;;  format like '(define (fn-name fn-args) fn-body)
(defn user-function-defined?
  [expr]
  (let [[x y & z] (vec expr)]
    (and (= x 'define)
         (list? y)
         (not (nil? z)))))


;; variable-defined?
;;  format like '(define x 5)
(defn variable-defined?
  [expr]
  (let [[x y & z] (vec expr)]
    (and (= x 'define)
         (symbol? y)
         (not (nil? z)))))

(defn is-keyword?
  [expr]
  (tagged-list? expr 'keyword))

(defn literal?
  [expr]
  (tagged-list? expr 'literal))

;; make-keyword:
;;  stored object: {:keyword '(keyword procedure-object)}
(defn make-keyword
  [proc]
  (list 'keyword proc))

(defn get-keyword-procedure
  [keyword-object]
  (second keyword-object))

;; make-literal
;; stored object: {:literal '(literal literal-value)}
(defn make-literal
  [literal-value]
  (list 'literal literal-value))

(defn get-literal-value
  [literal-object]
  (second literal-object))

;; initial global-env
(defn initialize-global-environment
  []
  (do
;;    (put! global-env 'and (make-built-in-function and))
;;    (put! global-env 'or (make-built-in-function or))
;;    (put! global-env 'not (make-built-in-function not))
    (put! global-env '+ (make-built-in-function +))
    (put! global-env '- (make-built-in-function -))
    (put! global-env '* (make-built-in-function *))
    (put! global-env '/ (make-built-in-function /))
    (put! global-env '> (make-built-in-function >))
    (put! global-env '< (make-built-in-function <))
    (put! global-env '= (make-built-in-function =))
    (put! global-env 'mod (make-built-in-function mod))
    (put! global-env 'cons (make-keyword cons-proc))
    (put! global-env 'car (make-keyword car-proc))
    (put! global-env 'cdr (make-keyword cdr-proc))
    (put! global-env 'list (make-keyword list-proc))
    (put! global-env 'true (make-literal true))
    (put! global-env 'false (make-literal false))))


;; apply function with arguments
(defn last-expression?
  [exprs]
  (= (count exprs) 1))

(defn first-expression
  [exprs]
  (first exprs))

(defn rest-expression
  [exprs]
  (rest exprs))

(defn eval-expressions
  [exprs env]
  (cond
   (last-expression? exprs) (eval1 (first-expression exprs) env)
   :else (do (eval1 (first-expression exprs) env)
             (eval-expressions (rest-expression exprs) env))))

(defn apply1
  [fn-object fn-args]
  (cond
   (built-in-function? fn-object) (apply (get-built-in-procedure fn-object) fn-args)
   (user-function? fn-object) (let [[_ fn-params fn-body] (vec fn-object)]
                                        (eval-expressions fn-body
                                                  (extend-environment fn-params
                                                                      fn-args
                                                                      (get-user-function-env fn-object))))
   (is-keyword? fn-object) (apply (get-keyword-procedure fn-object) fn-args)
   :else (throw (Exception. "Unknow type function -- APPLY1"))))

(defn eval1
  [expr env]
  (cond
   ;; basic expression
   (or (number? expr)
       (string? expr)
       (bool? expr)) expr
   ;; variable, function or literal
   (symbol? expr) (let [value (get env expr)]
                    (if (literal? value)
                      (get-literal-value value)
                      value))
   ;; define variable
   (variable-defined? expr) (let [[_ var & sub-exprs] (vec expr)]
                              (put! env var (eval1 (first-expression sub-exprs) env))
                              'ok)
   ;; define function
   (user-function-defined? expr) (let [[_ [fn-name & fn-params] & fn-body] (vec expr)]
                                   (put! env fn-name (make-user-function fn-params fn-body env))
                                   'ok)
   ;; call function
  (function-called? expr) (let [[fn-name & fn-args] (vec expr)
                                fn-object (get env fn-name)]
                            (apply1 fn-object fn-args))
  :else (throw (Exception. "Unknow eval type"))))

(defn repl
  []
  (print (str (ns-name *ns*) " >> "))
  (flush)
  (let [expr (read)
        value (eval1 expr global-env)]
    (when (not= value :quit)
      (prn value)
      (recur))))

(defn -main
  [& args]
  (initialize-global-environment)
  
  (repl))
