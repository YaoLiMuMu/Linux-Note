(require 'package)                      ;auto-load package
(add-to-list 'package-archives '("melpa" . "http://elpa.emacs-china.org/melpa/"))
(package-initialize)
(require 'cl)
(defvar my/packages '(			;packages list adn syc
		      company		;complete anything
		      ;; --- better editor ---
		      hungry-delete
		      counsel
		      swiper
		      smartparens
		      popwin
		      browse-kill-ring
		      magit
		      org-pomodoro
		      bing-dict
                      expand-region
                      iedit
                      auto-yasnippet
                      helm-ag
                      which-key
                      evil-nerd-commenter
		      ;; --- major mode ---
		      js2-mode
		      markdown-mode
                      xcscope
                      web-mode
                      htmlize
		      ;; --- python ide ---
		      elpy
		      flycheck
		      py-autopep8
		      ;; matlab-mode
                      ein
		      ;; --- minor mode ---
		      nodejs-repl
		      ;; exec-path-from-shell
		      ;; --- themes ---
		      monokai-theme
		      ;;solarized-theme
		      ) "Default packages")
(setq package-selected-packages my/packages)
(defun my/package-installed-p ()
  (loop for pkg in my/packages
	when (not (package-installed-p pkg)) do (return nil)
	finally (return t)))
(unless (my/package-installed-p)
  (message "%s" "Refreshing package database...")
  (package-refresh-contents)
  (dolist (pkg my/packages)
    (when (not (package-installed-p pkg))
      (package-install pkg))))
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(blink-cursor-mode t)
 '(company-idle-delay 0.2)
 '(company-minimum-prefix-length 2)
 '(menu-bar-mode nil)
 '(org-agenda-files
   '("~/Yaoli/GB Certification/test.org" "/home/madhouse/Yaoli/Org mode/Schedule.org" "/home/madhouse/Yaoli/Org mode/sticker.org"))
 '(package-selected-packages
   '(edit-indirect w3m company hungry-delete counsel swiper smartparens popwin browse-kill-ring magit org-pomodoro bing-dict expand-region iedit auto-yasnippet helm-ag which-key evil-nerd-commenter js2-mode markdown-mode xcscope web-mode elpy flycheck py-autopep8 ein nodejs-repl monokai-theme))
 '(popwin:popup-window-position 'right)
 '(popwin:popup-window-width 40)
 '(safe-local-variable-values
   '((TeX-engine . xetex)
     (TeX-master . t)
     (TeX-command-extra-options . "-shell-escape")))
 '(send-mail-function 'mailclient-send-it))
 ;'(session-use-package t nil (session)))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(region ((t (:inherit highlight :background "dark green")))))
;; Setting English Font
;;(set-face-attribute
;; 'default nil :font "Consolas-11")
;; Setting Chinese Font
;(dolist (charset '(kana han symbol cjk-misc bopomofo))
;  (set-fontset-font (frame-parameter nil 'font)
;                    charset
;                    (font-spec :family "Microsoft Yahei UI" :size 12)))
(set-language-environment "Chinese-GB")
(prefer-coding-system 'utf-8)
(set-language-environment 'utf-8)
(setq inhibit-startup-message t)
(tool-bar-mode -1)			;disable tool bar
(scroll-bar-mode -1)			;disable scroll bar
(global-linum-mode 1)			;turn on line number mode
(setq initial-scratch-message "Name: Madhouse 
Email: wo347522772@hotmail.com & yl347522772@gmail.com 
Tel: +8617689447702
")					;(setq inhibit-startup-message 1)
;;(setq frame-title-format "%b --The final death is when there is no one left in the living world who remembers you, you disappear")
;; a shortcut to set up to emacs
(defun open-my-file()
  (interactive)
  (find-file "/home/madhouse/.emacs"))
(global-set-key (kbd "<f12>") 'open-my-file)
(load-theme 'monokai 1)	        	;set default themes
(add-hook 'emacs-lisp-mode-hook 'show-paren-mode) ;show parens mode
;; show paren mode repair fix some smartparen quote issue
(define-advice show-paren-function (:around (fn) fix-show-paren-function)
  "Highlight enclosing parens."
  (cond ((looking-at-p "\\s(") (funcall fn))
	(t (save-excursion
	     (ignore-errors (backward-up-list))
	     (funcall fn)))))
(global-company-mode t)
;; enable smartparens
(add-hook 'js-mode-hook #'smartparens-mode)
(smartparens-global-mode 1)
(setq make-backup-files nil)		;disable backup file
(setq auto-save-default nil)		;disable auto-save
;; recent file
(recentf-mode 1)
(setq recentf-max-menu-items 20)
(global-set-key (kbd "M-s r") 'recentf-open-files)
(delete-selection-mode 1)
;; (setq visible-bell t)	 		;turn off alarm sound
;; (setq initial-frame-alist (quote ((fullscreen . maximized)))) ;fullscreen
;; highline in org mode
(require 'org)       
(setq org-src-fontify-natively t)
(global-hl-line-mode 1)			;hightlght current line
(defun chunyang-disable-hl-line-mode ()
(hl-line-mode -1))
(add-hook 'activate-mark-hook #'chunyang-disable-hl-line-mode)
(add-hook 'deactivate-mark-hook #'hl-line-mode)
;; org agenda file directory and keybindling
(setq org-agenda-files '("/home/madhouse/Yaoli/Org mode/"))
(global-set-key (kbd "C-c a") 'org-agenda)
;; use hungry-delete
(require 'hungry-delete)
(global-hungry-delete-mode)
;; counsel/ivy/swiper
(ivy-mode 1)
(setq ivy-use-virtual-buffers t)
(setq enable-recursive-minibuffers t)
(global-set-key "\C-s" 'swiper)
(global-set-key (kbd "C-c C-r") 'ivy-resume)
(global-set-key(kbd "M-x") 'counsel-M-x)
(global-set-key (kbd "C-x C-f") 'counsel-find-file)
(global-set-key (kbd "<f1> f") 'counsel-describe-function)
(global-set-key (kbd "<f1> v") 'counsel-describe-variable)
(global-set-key (kbd "<f1> l") 'counsel-find-library)
(global-set-key (kbd "<f2> i") 'counsel-info-lookup-symbol)
(global-set-key (kbd "<f2> u") 'counsel-unicode-char)
(global-set-key (kbd "C-c g") 'counsel-git)
(global-set-key (kbd "C-c j") 'counsel-git-grep)
(global-set-key (kbd "C-c k") 'counsel-ag)
(global-set-key (kbd "C-x l") 'counsel-locate)
(define-key minibuffer-local-map (kbd "C-r") 'counsel-minibuffer-history)
;; enable popwin-mode
(require 'popwin)
(popwin-mode 1)
(fset 'yes-or-no-p 'y-or-n-p)		;replace 'yes' and 'no'
;; set users information
(setq user-full-name "YaoLi")
(setq user-mail-address "wo347522772[AT]hotmail or yl347522772[AT]gmail.com")
;; abbreviation complete
(setq-default abbrev-mode t)
(define-abbrev-table 'global-abbrev-table '(
					    ("yl" "YaoLi")
					    ("ret" "<RET>")
					    ("mail1" "wo347522772@hotmail.com")
					    ("mail2" "yl347522772@gmail.com")
					    ("mail3" "347522772@qq.com")
					    ("mail4" "yao.lin1703@e-nebula.com")
					    ))
;; hippie company
(setq hippie-expand-try-function-list '(try-expand-debbrev
					try-expand-debbrev-all-buffers
					try-expand-debbrev-from-kill
					try-complete-file-name-partially
					try-complete-file-name
					try-expand-all-abbrevs
					try-expand-list
					try-expand-line
					try-complete-lisp-symbol-partially
					try-complete-lisp-symbol))
(global-set-key (kbd "M-/") 'hippie-expand)
;; dired mode
(require 'dired-x)
(put 'dired-find-alternate-file 'disabled nil)
(with-eval-after-load 'dired
  (define-key dired-mode-map (kbd "RET") 'dired-find-alternate-file))
(setq dired-dwin-target 1)
;; show-paren-mode repair
(define-advice show-paren-function (:around (fn) fix-show-paren-function)
  "Highlight enclosing parens."
  (cond ((looking-at-p "\\s(") (funcall fn))
	(t (save-excursion
	     (ignore-errors (backward-up-list))
	     (funcall fn)))))
;;set transparent effect
(global-set-key [(f11)] 'loop-alpha)
(setq alpha-list '((100 100) (95 65) (85 55) (75 45) (65 35)))
(defun loop-alpha ()
  (interactive)
  (let ((h (car alpha-list)))
    ;; head value will set to
    ((lambda (a ab)
       (set-frame-parameter (selected-frame) 'alpha (list a ab))
       (add-to-list 'default-frame-alist (cons 'alpha (list a ab)))
       ) (car h) (car (cdr h)))
    (setq alpha-list (cdr (append alpha-list (list h))))))
;default directoty
(defun my-find-file ()
  (interactive)
  (let ((default-directory "/home/madhouse/Yaoli/Org mode"))
    (call-interactively #'find-file)))
(global-set-key (kbd "C-x C-f") 'my-find-file)
;; activate python package
(elpy-enable)
;; python check
(when (require 'flycheck nil t)
  (setq elpy-modules (delq 'elpy-module-flymake elpy-modules))
  (add-hook 'elpy-mode-hook 'flycheck-mode))
;;(add-hook 'after-init-hook #'global-flycheck-mode)
(require 'py-autopep8)
(add-hook 'elpy-mode-hook 'py-autopep8-enable-on-save)
(setq py-autopep8-options '("--max-line-length=100"))
;; matlab-mode
;(autoload 'tlc-mode "tlc" "tlc Editing Mode" t)
;(add-to-list 'auto-mode-alist '("//.tlc$" . tlc-mode))
;(setq tlc-indent-function t)
;; enable dired to copy and delete directory
(setq dired-recursive-copies 'top)
(setq dired-recursive-deletes 'top)
;; turn on image view feature
(auto-image-file-mode t)
;; smoothly scroll 3 line
(setq scroll-margin 3
      scroll-conservatively 10000)
;; combination of desktop and session
;(desktop-save-mode 1)
;(require 'session)
;(add-hook 'after-init-hook 'session-initialize) 
;(add-to-list 'session-globals-exclude 'org-mark-ring)
(require 'ibuffer)			;ibuffer
(global-set-key (kbd "C-x C-b") 'ibuffer)
;; browse-kill-ring
(require 'browse-kill-ring)
(global-set-key [(control c)(k)] 'browse-kill-ring)
(browse-kill-ring-default-keybindings)
;; ido(interactively do)
(require 'ido)
(ido-mode t)
(setq ido-enable-flex-matching t)
(setq ido-use-filename-at-point 'guess) ;; guess filename according current sursor location
(setq ido-everywhere t)
(setq ido-file-extensions-order '(".org" ".txt" ".py" ".md" ".emacs" ".xml" ".e1" "ini" ".cfg" ".cnf" "" t))
;; quick search function in cuurent file
(defun js2-imenu-make-index ()
      (interactive)
      (save-excursion
	;; (setq imenu-generic-expression '((nil "describe\\(\"\\(.+\\)\"" 1)))
	(imenu--generic-function '(("describe" "\\s-*describe\\s-*(\\s-*[\"']\\(.+\\)[\"']\\s-*,.*" 1)
				   ("it" "\\s-*it\\s-*(\\s-*[\"']\\(.+\\)[\"']\\s-*,.*" 1)
				   ("test" "\\s-*test\\s-*(\\s-*[\"']\\(.+\\)[\"']\\s-*,.*" 1)
				   ("before" "\\s-*before\\s-*(\\s-*[\"']\\(.+\\)[\"']\\s-*,.*" 1)
				   ("after" "\\s-*after\\s-*(\\s-*[\"']\\(.+\\)[\"']\\s-*,.*" 1)
				   ("Function" "function[ \t]+\\([a-zA-Z0-9_$.]+\\)[ \t]*(" 1)
				   ("Function" "^[ \t]*\\([a-zA-Z0-9_$.]+\\)[ \t]*=[ \t]*function[ \t]*(" 1)
				   ("Function" "^var[ \t]*\\([a-zA-Z0-9_$.]+\\)[ \t]*=[ \t]*function[ \t]*(" 1)
				   ("Function" "^[ \t]*\\([a-zA-Z0-9_$.]+\\)[ \t]*()[ \t]*{" 1)
				   ("Function" "^[ \t]*\\([a-zA-Z0-9_$.]+\\)[ \t]*:[ \t]*function[ \t]*(" 1)
				   ("Task" "[. \t]task([ \t]*['\"]\\([^'\"]+\\)" 1)))))
(add-hook 'js2-mode-hook
	      (lambda ()
		(setq imenu-create-index-function 'js2-imenu-make-index)))
(global-set-key (kbd "M-s i") 'counsel-imenu)
;; pomodoro work
(require 'org-pomodoro)
(setq org-capture-templates
      '(("t" "Todo" entry (file+headline "/home/madhouse/Yaoli/Org mode/Templates/GTD.org" "Getting Things Done")
	 "* TODO [#B] %?\n  %i\n"
	 :empty-lines 1)))
(global-set-key (kbd "C-c r") 'org-capture)
;; bing-translate
(global-set-key (kbd "C-c d") 'bing-dict-brief)
(setq bing-dict-save-search-result t)
(setq bing-dict-org-file "/home/madhouse/Note/vocabulary.org")
(setq default-major-mode 'text-mode)	;text mode repalce fundamental-mode
(mouse-avoidance-mode 'animate)		;cursor and mouse
(put 'set-goal-column 'disabled nil)	;ebable set-goal-column
(setq sentence-end "\\([。！？]\\|……\\|[.?!][]\"')}]*\\($\\|[ \t]\\)\\)[ \t\n]*") ;combination of Chinese punctuation
;; enable auto fill mode
(global-set-key (kbd "C-c q") 'auto-fill-mode)
(setq comment-auto-fill-only-comments t)
(setq adaptive-fill-regexp "[ \t]+\\|[ \t]*\\([0-9]+\\.\\|\\*+\\)[ \t]*")
(setq adaptive-fill-first-line-regexp "^\\* *$")
;; enable upcase and downcase feature
(put 'upcase-region 'disabled nil) 
(put 'downcase-region 'disabled nil)
(display-time-mode 1)			;enable time display
(setq display-time-day-and-date t)	;display Date, Day and Time
(setq display-time-use-mail-icon t)	;enable mail setting close to minibuffer time bar
(setq display-time-interval 10)		;set time refresh frequency
(setq ido-save-directory-list-file nil) ;don't save ido mode directory list
(setq-default indent-tabs-mode nil)
;; encryption display password when shell, telnet and w3m modes
(add-hook 'comint-output-filter-functions
	  'comint-watch-for-password-prompt)
(setq track-eol t)                      ;sursor piont on end of line when moviing up and down
(global-set-key [f9] 'undo)             ;bind [f9] undoes
(global-set-key [f8] 'calendar)         ;bind [f8] calendar, customize color, location
(setq calendar-load-hook
      '(lambda ()
         (set-face-foreground 'diary-face "skyblue")
         (set-face-background 'holiday-face "slate blue")
         (set-face-foreground 'holiday-face "white")))
(setq calendar-latitude +26.10)
(setq calendar-longitude +119.28)
(setq calendar-location-name "FuZhou")  ;on calendar interface type <S> view sunrise and sunset time
(setq calendar-remove-frame-by-deleting t)
(setq mark-diary-entries-in-calendar t)
(setq christian-holidays nil)
(setq hebrew-holidays nil)
(setq islamic-holidays nil)
(setq solar-holidays nil)
(setq holiday-other-holidays '((holiday-fixed 5 1 "Labor Day")
                               (holiday-fixed 6 1 "Children's Day")))
;; fold code
(load-library "hideshow")
(add-hook 'c-mode-hook 'hs-minor-mode)
(add-hook 'c++-mode-hook 'hs-minor-mode)
(add-hook 'java-mode-hook 'hs-minor-mode)
(add-hook 'perl-mode-hook 'hs-minor-mode)
(add-hook 'php-mode-hook 'hs-minor-mode)
(add-hook 'emacs-lisp-mode-hook 'hs-minor-mode)
;; cscope for emacs
(require 'xcscope)
(cscope-setup)
(global-auto-revert-mode t)             ;auto revert configuration file
;; indent buffer batter
(defun indent-buffer()
  (interactive)
  (indent-region (point-min) (point-max)))
(defun indent-region-or-buffer()
  (interactive)
  (save-excursion
    (if (region-active-p)
	(progn
	  (indent-region (region-beginning) (region-end))
	  (message "Indent selected region."))
      (progn
	(indent-buffer)
	(message "Indent buffer.")))))
(global-set-key (kbd "C-M-\\") 'indent-region-or-buffer)
(sp-local-pair '(emacs-lisp-mode lisp-interaction-mode) "'" nil :actions nil)
(setq auto-mode-alist                   ;call js2-mode and web-mode when open js file/html file
      (append
       '(("\\.js\\'" . js2-mode))
       '(("\\.html\\'" . web-mode))
;       '(("\\.ahk\\'" . ahk-mode))      ;ahk file to ahk-mode
       auto-mode-alist))
(defun my-web-mode-indent-setup ()
  (setq web-mode-markup-indent-offset 2) ; web-mode, html tag in html file
  (setq web-mode-css-indent-offset 2)    ; web-mode, css in html file
  (setq web-mode-code-indent-offset 2)   ; web-mode, js code in html file
  )
(add-hook 'web-mode-hook 'my-web-mode-indent-setup)
(defun my-toggle-web-indent ()
  (interactive)
  ;; web development
  (if (or (eq major-mode 'js-mode) (eq major-mode 'js2-mode))
      (progn
	(setq js-indent-level (if (= js-indent-level 2) 4 2))
	(setq js2-basic-offset (if (= js2-basic-offset 2) 4 2))))
  (if (eq major-mode 'web-mode)
      (progn (setq web-mode-markup-indent-offset (if (= web-mode-markup-indent-offset 2) 4 2))
	     (setq web-mode-css-indent-offset (if (= web-mode-css-indent-offset 2) 4 2))
	     (setq web-mode-code-indent-offset (if (= web-mode-code-indent-offset 2) 4 2))))
  (if (eq major-mode 'css-mode)
      (setq css-indent-offset (if (= css-indent-offset 2) 4 2)))
  (setq indent-tabs-mode nil))
(global-set-key (kbd "C-c t i") 'my-toggle-web-indent)
;(defun occur-dwim ()
;  "Call `occur' with a sane default."
;  (interactive)
;  (push (if (region-active-p)
;	    (buffer-substring-no-properties
;	     (region-beginning)
;	     (region-end))
;	  (let ((sym (thing-at-point 'symbol)))
;	    (when (stringp sym)
;	      (regexp-quote sym))))
;	regexp-history)
;  (call-interactively 'occur))
;(global-set-key (kbd "M-s o") 'occur-dwim)
(global-set-key (kbd "C-=") 'er/expand-region)
(global-set-key (kbd "M-s e") 'iedit-mode)
(with-eval-after-load 'company
  (define-key company-active-map (kbd "M-n") nil)
  (define-key company-active-map (kbd "M-p") nil)
  (define-key company-active-map (kbd "C-n") #'company-select-next)
  (define-key company-active-map (kbd "C-p") #'company-select-previous))
(yas-reload-all)
(add-hook 'prog-mode-hook #'yas-minor-mode)
(global-set-key (kbd "H-w") #'aya-create)
(global-set-key (kbd "H-y") #'aya-expand)
(global-set-key (kbd "C-w") 'backward-kill-word)
(global-set-key (kbd "C-c p s") 'helm-do-ag-project-root)
(global-set-key (kbd "C-x g") 'magit-status)
(which-key-mode 1)
(evilnc-default-hotkeys)
(server-start)
(defun qiang-comment-dwim-line (&optional arg)
  (interactive "*P")
  (comment-normalize-vars)
  (if (and (not (region-active-p)) (not (looking-at "[ \t]*$")))
      (comment-or-uncomment-region (line-beginning-position) (line-end-position))
    (comment-dwim arg)))
(global-set-key "\M-;" 'qiang-comment-dwim-line)
(defun middle-of-line ()
  "Put cursor at the middle point of the line."
  (interactive)
  (goto-char (/ (+ (point-at-bol) (point-at-eol)) 2)))
(global-set-key (kbd "C-i") 'middle-of-line)
(defun insert-current-date ()
  "Insert the current date15:55:11"
  (interactive "*")
;(insert (format-time-string "%Y/%m/%d %H:%M:%S" (current-time))))
  (insert (format-time-string "%Y/%m/%d" (current-time))))
(global-set-key "\M-sd" 'insert-current-date)
(defun insert-current-time ()
  "Insert the current time"
  (interactive "*")
;(insert (format-time-string "%Y/%m/%d %H:%M:%S" (current-time))))
  (insert (format-time-string "%H:%M:%S" (current-time))))
(global-set-key "\M-st" 'insert-current-time)
;; latex mode 
(add-hook 'LaTeX-mode-hook (lambda()
(add-to-list 'TeX-command-list '("XeLaTeX" "%`xelatex%(mode)%' %t" TeX-run-TeX nil t))
(setq TeX-command-default "XeLaTeX")
(setq TeX-save-query  nil )
(setq TeX-show-compilation t)
))
;; org latex size
(require 'org)
(setq org-format-latex-options (plist-put org-format-latex-options :scale 2.0))
;;
;;;;;;;;;;;;;;;;;
;auctex
;;;;;;;;;;;;;;;;;
;; (load "auctex.el" nil t t)
;; (load "preview-latex.el" nil t t)
;; (setq TeX-auto-save t)
;; (setq TeX-parse-self t)
;; (setq-default TeX-master nil)
;; (mapc (lambda (mode)
;; (add-hook 'LaTeX-mode-hook mode))
      ;; (list 'auto-complete-mode
   ;; 'auto-fill-mode
   ;; 'LaTeX-math-mode
   ;; 'turn-on-reftex                      
   ;; 'linum-mode))
;; (add-hook 'LaTeX-mode-hook
          ;; (lambda ()
            ;; (setq TeX-auto-untabify t     ; remove all tabs before saving
                  ;; TeX-engine 'xetex       ; use xelatex default
                  ;; TeX-show-compilation t) ; display compilation windows
            ;; (TeX-global-PDF-mode t)       ; PDF mode enable, not plain
            ;; (setq TeX-save-query nil)
            ;; (imenu-add-menubar-index)
            ;; (define-key LaTeX-mode-map (kbd "TAB") 'TeX-complete-symbol)))
; set pdf view tool
;; (setq TeX-view-program-list '(("Evince" "evince %o")))
;; (cond                                   ;
 ;; ((eq system-type 'windows-nt)
  ;; (add-hook 'LaTeX-mode-hook
            ;; (lambda ()
              ;; (setq TeX-view-program-selection '((output-pdf "SumatraPDF")
                                                 ;; (output-dvi "Yap"))))))

 ;; ((eq system-type 'gnu/linux)
  ;; (add-hook 'LaTeX-mode-hook
            ;; (lambda ()
              ;; (setq TeX-view-program-selection '((output-pdf "Evince")
                                                 ;; (output-dvi "Evince")))))))
; XeLaTeX
;; (add-hook 'LaTeX-mode-hook (lambda()
;;     (add-to-list 'TeX-command-list '("XeLaTeX" "%`xelatex%(mode)%' %t" TeX-run-TeX nil t))
;;     (setq TeX-command-default "XeLaTeX")
;;     (setq TeX-save-query  nil )
;;     (setq TeX-show-compilation t)
;;     ))
  ;; ;; 使用xelatex一步生成PDF，不是org-latex-to-pdf-process这个命令
  ;; (setq org-latex-pdf-process
  ;;       '(
  ;;         "xelatex -shell-escape -interaction nonstopmode -output-directory %o %f"
  ;;         "xelatex -shell-escape -interaction nonstopmode -output-directory %o %f"
  ;;         "xelatex -shell-escape -interaction nonstopmode -output-directory %o %f"
  ;;         "rm -fr %b.out %b.log %b.tex auto"
  ;;         ))
;;   ;; 设置默认后端为 `xelatex'
(setq org-latex-compiler "xelatex")
;; ;; -- Display images in org mode
;; ;; enable image mode first
;; (iimage-mode)
;; ;; add the org file link format to the iimage mode regex
;; (add-to-list 'iimage-mode-image-regex-alist
;;   (cons (concat "\\[\\[file:\\(~?" iimage-mode-image-filename-regex "\\)\\]")  1))
;; ;;  add a hook so we can display images on load
;; (add-hook 'org-mode-hook '(lambda () (org-turn-on-iimage-in-org)))
;; ;; function to setup images for display on load
;; (defun org-turn-on-iimage-in-org ()
;;   "display images in your org file"
;;   (interactive)
;;   (turn-on-iimage-mode)
;;   (set-face-underline-p 'org-link nil))
;; ;; function to toggle images in a org bugger
;; (defun org-toggle-iimage-in-org ()
;;   "display images in your org file"
;;   (interactive)
;;   (if (face-underline-p 'org-link)
;;       (set-face-underline-p 'org-link nil)
;;       (set-face-underline-p 'org-link t))
;;   (call-interactively 'iimage-mode))
;; (load "auctex.el" nil t t)
;; (load "preview-latex.el" nil t t)
;; (setq tex-auto-save t)
;; (setq tex-parse-self t)
;; (setq-default tex-master nil)
;; font config for org table showing.
;; (set-default-font "monospace-11")
;; (dolist (charset '(kana han symbol cjk-misc bopomofo))
;;    (set-fontset-font (frame-parameter nil 'font)
;;                      charset
;;                      (font-spec :family "WenQuanYi Micro Hei")))
;; ;; tune rescale so that Chinese character width = 2 * English character width
;; (setq face-font-rescale-alist '(("monospace" . 1.0) ("WenQuanYi" . 1.23)))
;; w3m
(require 'w3m)
(setq w3m-home-page "http://www.baidu.com") 
(setq w3m-default-display-inline-images t)
(setq w3m-default-toggle-inline-images t)
;;显示图标  
(setq w3m-show-graphic-icons-in-header-line t) 
(setq w3m-show-graphic-icons-in-mode-line t)
;;启用cookie  
(setq w3m-use-cookies t)
;设定w3m运行的参数，分别为使用cookie和使用框架 
(setq w3m-command-arguments '("-cookie" "-F"))
(setq org-enforce-todo-dependencies t)
(setq org-default-notes-file (concat org-directory "~/Yaoli/ideaCapture.org")) 
(define-key global-map "\C-cc" 'org-capture)

(setq org-agenda-ndays 30)
(setq org-agenda-include-diary t)


;(setq markdown-command "/usr/bin/pandoc/")
(setq markdown-command
      (concat
       "/usr/bin/pandoc"
       " --from=markdown --to=html5"
       " --standalone --mathjax --highlight-style=pygments"))

(setq org-plantuml-jar-path
      (expand-file-name "/home/madhouse/Downloads/plantuml.jar"))

;; use plantuml as org-babel language

(org-babel-do-load-languages 'org-babel-load-languages '((plantuml . t)))

;; helper function

(defun my-org-confirm-babel-evaluate (lang body)

"Do not ask for confirmation to evaluate code for specified languages."

(member lang '("plantuml")))

;; trust certain code as being safe

(setq org-confirm-babel-evaluate 'my-org-confirm-babel-evaluate)

;; automatically show the resulting image

(add-hook 'org-babel-after-execute-hook 'org-display-inline-images)

;; active Org-babel languages
(with-eval-after-load 'org
(org-babel-do-load-languages
 'org-babel-load-languages
 '(;; other Babel languages
   (R . t)
   (shell . t)
   (python . t)
   (octave . t)
   (plantuml . t))))
(setq org-plantuml-jar-path
      (expand-file-name "/home/madhouse/Downloads/plantuml.jar"))
;; Enable plantuml-mode for PlantUML files
(add-to-list 'auto-mode-alist '("\\.plantuml\\'" . plantuml-mode))
;; Integration with org-mode
(add-to-list 'org-src-lang-modes '("plantuml" . plantuml))

;; htmlize
(require 'htmlize)
;; ox-freemind export
(add-to-list 'load-path "~/.emacs.d/elpa/ox-freemind")
(require 'ox-freemind)
;;(setq org-export-backends '(freemind odt latex icalendar html ascii))
(setq debug-on-error t)
