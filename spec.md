# Feature Specification: Gestion de projets Pixel & Co.

**Feature Branch**: `[project-management-app]`

**Created**: 22 mai 2026

**Status**: Draft

**Input**: Description du besoin pour une application web de gestion de projets interne et client pour Pixel & Co., avec une base de données stockée en fichiers binaires locaux.

## 1. Objectif général

L’application doit fournir une plateforme web centralisée permettant à Pixel & Co. de gérer les projets internes et clients, les backlogs, les tâches, les user stories, les responsabilités, les échéances, les notifications et les tableaux de bord de suivi.

L’objectif est de remplacer l’utilisation dispersée de tableurs, e-mails et réunions informelles par un outil unique offrant une meilleure visibilité, une collaboration structurée et un suivi opérationnel quotidien.

## 2. Acteurs principaux

- **Chef de projet**: crée, modifie, priorise et suit les projets. Gère les tâches et l’affectation des membres.
- **Développeur**: consulte les tâches assignées, met à jour le statut, enrichit les descriptions techniques et contribue aux user stories.
- **Membre de l’équipe**: consulte les projets et tâches concernés, reçoit des notifications et suit l’avancement.
- **Administrateur**: gère les utilisateurs, les rôles, les permissions et les paramètres globaux.

## 3. User Stories prioritaires

### User Story 1 - Gestion complète d’un projet (Priority: P1)

En tant que chef de projet, je veux créer un projet avec ses informations clés, y associer des membres et des tâches, puis suivre son état depuis un tableau de bord afin d’organiser le travail de l’équipe.

**Why this priority**: C’est la fonction cœur qui permet de remplacer les tableurs et d’organiser le travail.

**Independent Test**: Vérifier qu’un projet peut être créé, modifié, consulté, archivé et que ses tâches et membres sont affichés correctement.

**Acceptance Scenarios**:
1. **Given** un chef de projet authentifié, **When** il crée un projet avec nom, description et date de livraison, **Then** le projet existe et apparaît dans la liste des projets.
2. **Given** un projet existant, **When** il est archivé, **Then** il n’apparaît plus dans la vue principale des projets actifs.
3. **Given** un projet actif, **When** des membres sont ajoutés, **Then** seuls ces membres peuvent accéder au projet.

---

### User Story 2 - Suivi des tâches assignées (Priority: P1)

En tant que développeur, je veux consulter les tâches qui me sont assignées, mettre à jour leur statut et ajouter des commentaires afin de suivre mon travail.

**Why this priority**: Permet la collaboration et le suivi opérationnel des tâches quotidiennes.

**Independent Test**: Vérifier l’accès à la liste des tâches assignées, le changement de statut et l’ajout de commentaires.

**Acceptance Scenarios**:
1. **Given** un développeur connecté, **When** il consulte ses tâches assignées, **Then** il reçoit la liste des tâches affectées à son compte.
2. **Given** une tâche assignée, **When** il change le statut en "en cours" puis "terminée", **Then** le statut est mis à jour et enregistré.

---

### User Story 3 - Tableau de bord visuel (Priority: P2)

En tant que membre de l’équipe, je veux voir un tableau de bord qui présente l’état des projets, les tâches urgentes et les échéances proches afin d’identifier rapidement les priorités.

**Why this priority**: Permet la visualisation rapide de l’avancement et des risques.

**Independent Test**: Vérifier que le tableau de bord affiche les indicateurs clés et qu’il est filtrable par projet et utilisateur.

**Acceptance Scenarios**:
1. **Given** un utilisateur avec accès à plusieurs projets, **When** il ouvre le tableau de bord, **Then** il voit des cartes ou graphiques montrant les tâches par statut et les échéances.
2. **Given** des tâches à échéance proche, **When** elles sont détectées, **Then** elles apparaissent comme « échéance approche » ou « en retard ».

---

### User Story 4 - Gestion des permissions (Priority: P2)

En tant qu’administrateur, je veux gérer les comptes utilisateur, les rôles et les permissions afin de sécuriser l’accès aux projets et aux données.

**Why this priority**: Assure une sécurité minimale et un contrôle d’accès approprié.

**Independent Test**: Vérifier la création de comptes, la modification de rôles et le contrôle d’accès entre utilisateurs autorisés et non autorisés.

**Acceptance Scenarios**:
1. **Given** un administrateur, **When** il crée un utilisateur et lui assigne un rôle, **Then** l’utilisateur peut se connecter et voir l’interface correspondant à son rôle.
2. **Given** un utilisateur non associé à un projet, **When** il tente d’accéder au projet, **Then** l’accès est refusé.

---

### User Story 5 - Historique et traçabilité (Priority: P3)

En tant que chef de projet, je veux consulter l’historique des modifications d’un projet, d’une tâche ou d’une user story afin de comprendre les changements et le contexte.

**Why this priority**: Permet la traçabilité et la transparence des évolutions.

**Independent Test**: Vérifier qu’un log de modifications est enregistré et consultable pour chaque entité.

**Acceptance Scenarios**:
1. **Given** une tâche modifiée, **When** l’historique est consulté, **Then** il affiche l’auteur, la date et la nature du changement.

## 4. Edge Cases

- Tentative d’accès à un projet non autorisé doit revenir une erreur d’accès sans fuite d’information.
- Tâche sans responsable doit être clairement signalée et reste assignable.
- Une tâche terminée ne doit plus apparaître comme en retard.
- Lorsqu’une dépendance de tâche obligatoire n’est pas complétée, la tâche dépendante ne peut pas être marquée comme terminée.
- Archivage d’un projet doit verrouiller les tâches associées pour les utilisateurs non autorisés.

## 5. Exigences fonctionnelles

### 5.1 Gestion des utilisateurs

- **FR-001**: Authentification des utilisateurs via identifiants valides.
- **FR-002**: Déconnexion sécurisée des utilisateurs.
- **FR-003**: Gestion de rôles: administrateur, chef de projet, développeur, membre de l’équipe.
- **FR-004**: Application de permissions basées sur le rôle.
- **FR-005**: Administration des comptes utilisateurs: créer, modifier, désactiver, supprimer.
- **FR-006**: Attribution d’un ou plusieurs rôles à un utilisateur.
- **FR-007**: Association d’utilisateurs à un ou plusieurs projets.
- **FR-008**: Blocage d’accès aux projets non associés.

### 5.2 Gestion des projets

- **FR-009**: Création de projets par le chef de projet.
- **FR-010**: Saisie d’au moins un nom, une description et une date de livraison à la création.
- **FR-011**: Modification des informations d’un projet.
- **FR-012**: Suppression ou archivage d’un projet.
- **FR-013**: Consultation de la liste des projets en cours pour les utilisateurs autorisés.
- **FR-014**: Consultation des détails d’un projet.
- **FR-015**: Affichage des statuts de projet (non démarré, en cours, en attente, terminé, archivé).
- **FR-016**: Filtrage des projets par statut, date de livraison, responsable et priorité.
- **FR-017**: Recherche de projets par nom ou mot-clé.
- **FR-018**: Association de membres à un projet.
- **FR-019**: Retrait de membres d’un projet avec permissions appropriées.
- **FR-020**: Historique des principales modifications d’un projet.

### 5.3 Gestion du backlog

- **FR-021**: Création d’un backlog pour chaque projet.
- **FR-022**: Ajout de tâches au backlog.
- **FR-023**: Modification des tâches du backlog.
- **FR-024**: Suppression ou archivage de tâches.
- **FR-025**: Priorisation des tâches.
- **FR-026**: Classification des priorités: faible, moyenne, élevée, critique.
- **FR-027**: Modification du statut d’une tâche.
- **FR-028**: Prise en charge des statuts: à faire, en cours, en révision, bloquée, terminée, annulée.
- **FR-029**: Filtrage des tâches par statut, priorité, responsable, date limite ou projet.
- **FR-030**: Recherche de tâches par titre, description ou mot-clé.
- **FR-031**: Réorganisation du backlog selon importance ou ordre d’exécution.
- **FR-032**: Distinction visuelle des tâches urgentes.
- **FR-033**: Indication claire des tâches en retard.
- **FR-034**: Liaison des tâches à une ou plusieurs user stories.
- **FR-035**: Estimation d’effort pour chaque tâche (heures, points, unité d’équipe).
- **FR-036**: Définition d’une date limite par tâche.
- **FR-037**: Ajout de commentaires aux tâches.
- **FR-038**: Consultation de l’historique des changements d’une tâche.

### 5.4 Gestion des tâches

- **FR-039**: Création de tâches dans un projet par un utilisateur autorisé.
- **FR-040**: Une tâche doit contenir titre, description, statut, priorité et projet associé.
- **FR-041**: Assignation des tâches à un membre de l’équipe.
- **FR-042**: Modification de l’assignation.
- **FR-043**: Retrait de l’assignation.
- **FR-044**: Mise à jour du statut par l’utilisateur assigné.
- **FR-045**: Modification de toutes les tâches du projet par le chef de projet responsable.
- **FR-046**: Identification des tâches bloquées.
- **FR-047**: Enregistrement de la raison d’un blocage.
- **FR-048**: Ajout de dépendances entre tâches.
- **FR-049**: Blocage de la clôture d’une tâche dépendante si les dépendances ne sont pas terminées.
- **FR-050**: Jointure de fichiers ou de liens à une tâche.
- **FR-051**: Consultation de toutes les tâches assignées à un utilisateur.
- **FR-052**: Consultation de toutes les tâches non assignées d’un projet.
- **FR-053**: Modification de la priorité en cours de projet.
- **FR-054**: Marquage d’une tâche comme terminée.
- **FR-055**: Conservation de la date de création et de la date de dernière modification.

### 5.5 Gestion des user stories

- **FR-056**: Création de user stories dans un projet.
- **FR-057**: Une user story doit contenir titre, description, acteur, besoin et résultat attendu.
- **FR-058**: Rédaction structurée de la user story (format "En tant que ...").
- **FR-059**: Modification des user stories existantes.
- **FR-060**: Suppression ou archivage de user stories.
- **FR-061**: Association des user stories aux tâches.
- **FR-062**: Priorisation des user stories.
- **FR-063**: Statut des user stories: proposée, validée, en développement, terminée, rejetée.
- **FR-064**: Ajout de critères d’acceptation.
- **FR-065**: Consultation des user stories par projet.
- **FR-066**: Filtrage des user stories par statut, priorité, acteur ou projet.
- **FR-067**: Liaison des user stories à une fonctionnalité ou un objectif.
- **FR-068**: Historique des modifications importantes des user stories.

### 5.6 Attribution des responsabilités

- **FR-069**: Assignation de chaque tâche à un membre de l’équipe.
- **FR-070**: Consultation rapide du responsable d’une tâche.
- **FR-071**: Modification du responsable d’une tâche par le chef de projet.
- **FR-072**: Visualisation de la liste des responsabilités actuelles d’un utilisateur.
- **FR-073**: Affichage des tâches par utilisateur.
- **FR-074**: Détection des tâches sans responsable.
- **FR-075**: Détection des utilisateurs en surcharge selon nombre de tâches ou effort.
- **FR-076**: Visualisation de la répartition des tâches entre membres.

### 5.7 Gestion des échéances

- **FR-077**: Définition d’une date limite pour chaque tâche.
- **FR-078**: Modification de la date limite d’une tâche.
- **FR-079**: Indication claire des échéances proches.
- **FR-080**: Indication claire des tâches en retard.
- **FR-081**: Filtrage des tâches par date limite.
- **FR-082**: Tri des tâches par urgence.
- **FR-083**: Visualisation des échéances importantes d’un projet.
- **FR-084**: Indication de la date de livraison prévue d’un projet.
- **FR-085**: Identification des projets dont la livraison approche.
- **FR-086**: Identification des projets en retard.

### 5.8 Notifications

- **FR-087**: Notification lors de l’assignation d’une tâche.
- **FR-088**: Notification pour modification importante d’une tâche assignée.
- **FR-089**: Notification pour échéance proche.
- **FR-090**: Notification lorsqu’une tâche devient en retard.
- **FR-091**: Consultation des notifications dans l’application.
- **FR-092**: Marquage des notifications comme lues.
- **FR-093**: Différenciation entre notifications lues et non lues.
- **FR-094**: Configuration de préférences de notification selon règles de l’organisation.
- **FR-095**: Évitement des notifications redondantes pour un même événement.
- **FR-096**: Conservation d’un historique minimal des notifications récentes.

### 5.9 Tableau de bord

- **FR-097**: Tableau de bord interactif de suivi des projets.
- **FR-098**: Affichage du nombre total de tâches par projet.
- **FR-099**: Affichage du nombre de tâches par statut.
- **FR-100**: Affichage des tâches urgentes.
- **FR-101**: Affichage des tâches récemment mises à jour.
- **FR-102**: Affichage des projets dont la livraison approche.
- **FR-103**: Filtrage du tableau de bord par projet.
- **FR-104**: Filtrage du tableau de bord par utilisateur.
- **FR-105**: Filtrage du tableau de bord par statut ou priorité.
- **FR-106**: Présentation visuelle claire (cartes, graphiques, listes, indicateurs).
- **FR-107**: Identification rapide des actions prioritaires.
- **FR-108**: Mise à jour automatique ou régulière des données.
- **FR-109**: Accès direct aux détails d’un projet ou d’une tâche depuis le tableau de bord.

### 5.10 Collaboration

- **FR-110**: Commentaires sur les tâches.
- **FR-111**: Commentaires sur les user stories.
- **FR-112**: Affichage de l’auteur et de la date de chaque commentaire.
- **FR-113**: Mentions de membres dans les commentaires, si activé.
- **FR-114**: Notification lors d’une mention.
- **FR-115**: Centralisation des informations de projet.
- **FR-116**: Consultation de l’historique d’activité d’un projet.
- **FR-117**: Consultation des changements récents sur un projet.

### 5.11 Recherche, filtres et tri

- **FR-118**: Recherche de projets par nom, description ou mot-clé.
- **FR-119**: Recherche de tâches par titre, description, responsable ou mot-clé.
- **FR-120**: Recherche de user stories par titre, acteur, besoin ou mot-clé.
- **FR-121**: Filtrage des tâches par statut.
- **FR-122**: Filtrage des tâches par priorité.
- **FR-123**: Filtrage des tâches par responsable.
- **FR-124**: Filtrage des tâches par échéance.
- **FR-125**: Tri des tâches par priorité, date limite, statut ou date de modification.
- **FR-126**: Sauvegarde ou réutilisation de filtres fréquents si prévu.

### 5.12 Historique et traçabilité

- **FR-127**: Historique des modifications importantes des projets.
- **FR-128**: Historique des modifications importantes des tâches.
- **FR-129**: Historique des modifications importantes des user stories.
- **FR-130**: Historique incluant l’utilisateur, la date et la nature du changement.
- **FR-131**: Consultation de l’historique d’un projet par les utilisateurs autorisés.
- **FR-132**: Consultation de l’historique d’une tâche par les utilisateurs autorisés.
- **FR-133**: Consultation de l’historique d’une user story par les utilisateurs autorisés.

## 6. Exigences non fonctionnelles

### 6.1 Sécurité

- **NFR-134**: Authentification pour protéger l’accès aux données.
- **NFR-135**: Contrôle d’accès par rôles et permissions.
- **NFR-136**: Blocage de l’accès aux ressources non autorisées.
- **NFR-137**: Stockage sécurisé des mots de passe par hachage.
- **NFR-138**: Utilisation de HTTPS en production.
- **NFR-139**: Validation des données saisies pour prévenir les entrées invalides ou malveillantes.
- **NFR-140**: Journalisation des événements de sécurité importants.
- **NFR-141**: Limitation des informations sensibles dans les messages d’erreur.

### 6.2 Performance

- **NFR-142**: Chargement acceptable des pages principales.
- **NFR-143**: Consultation fluide des projets, tâches et tableaux de bord pour plusieurs utilisateurs.
- **NFR-144**: Conception évolutive pour gérer croissance de projets, tâches et utilisateurs.
- **NFR-145**: Optimisation des requêtes de recherche, filtrage et tri.
- **NFR-146**: Chargement rapide des indicateurs du tableau de bord.
- **NFR-147**: Minimisation des rechargements complets inutiles.

### 6.3 Fiabilité

- **NFR-148**: Conservation des données en cas d’erreur applicative contrôlée.
- **NFR-149**: Gestion claire des erreurs pour l’utilisateur.
- **NFR-150**: Protection contre la perte de données lors d’opérations critiques.
- **NFR-151**: Confirmation des actions destructrices.
- **NFR-152**: Archivage des projets et tâches au lieu de suppression définitive lorsque nécessaire.
- **NFR-153**: Mécanisme de sauvegarde des données en production.
- **NFR-154**: Récupération possible depuis une sauvegarde selon les procédures définies.

### 6.4 Utilisabilité

- **NFR-155**: Interface claire, cohérente et facile à utiliser.
- **NFR-156**: Facilitation de la découverte des projets et des tâches pour un nouvel utilisateur.
- **NFR-157**: Réduction du nombre d’actions pour consulter les tâches prioritaires.
- **NFR-158**: Messages d’erreur clairs en cas d’échec.
- **NFR-159**: Indicateurs visuels pour tâches urgentes, en retard ou bloquées.
- **NFR-160**: Navigation rapide entre projets, tâches, user stories et tableau de bord.
- **NFR-161**: Utilisation adaptée aux ordinateurs portables et écrans de bureau.
- **NFR-162**: Adaptation possible aux appareils mobiles ou tablettes si prévu.

### 6.5 Accessibilité

- **NFR-163**: Respect des bonnes pratiques d’accessibilité web.
- **NFR-164**: Contraste suffisant texte/arrière-plan.
- **NFR-165**: Navigation au clavier pour les actions principales.
- **NFR-166**: Libellés clairs pour les champs de formulaire.
- **NFR-167**: Ne pas transmettre l’information uniquement par la couleur.
- **NFR-168**: Textes alternatifs pour éléments visuels significatifs.

### 6.6 Maintenabilité

- **NFR-169**: Architecture claire séparant responsabilités.
- **NFR-170**: Facilité d’ajout de nouvelles fonctionnalités sans refonte majeure.
- **NFR-171**: Code structuré et documenté.
- **NFR-172**: Conventions de nommage uniformes.
- **NFR-173**: Tests automatisés pour fonctionnalités critiques.
- **NFR-174**: Configuration distincte pour développement, test et production.
- **NFR-175**: Versionnement avec contrôle de code source.

### 6.7 Compatibilité

- **NFR-176**: Compatibilité avec navigateurs web modernes.
- **NFR-177**: Utilisabilité sur systèmes d’exploitation courants via navigateur.
- **NFR-178**: Application web accessible sans installation locale obligatoire.
- **NFR-179**: Déploiement possible dans un environnement serveur ou infonuagique standard.

### 6.8 Confidentialité et protection des données

- **NFR-180**: Protection des données projet contre accès non autorisé.
- **NFR-181**: Limitation de l’accès aux informations internes aux utilisateurs autorisés.
- **NFR-182**: Désactivation d’un utilisateur sans suppression automatique de l’historique de ses actions.
- **NFR-183**: Conservation des données selon les règles définies par l’organisation.
- **NFR-184**: Exportation des données pertinentes si nécessaire.

## 7. Requis de données

- **DR-185**: Stockage des informations utilisateur: nom, courriel, rôle, statut de compte.
- **DR-186**: Stockage des informations projet: nom, description, date de livraison, statut, membres associés.
- **DR-187**: Stockage des informations tâche: titre, description, statut, priorité, responsable, date limite, projet associé.
- **DR-188**: Stockage des informations user story: titre, acteur, besoin, résultat attendu, critères d’acceptation, projet associé.
- **DR-189**: Stockage des commentaires associés aux tâches et user stories.
- **DR-190**: Stockage des notifications destinées aux utilisateurs.
- **DR-191**: Stockage de l’historique des modifications importantes.
- **DR-192**: Intégrité des relations entre projets, tâches, user stories, utilisateurs et notifications.
- **DR-193**: Empêchement de la création de données incohérentes comme une tâche sans projet.

### 7.1 Base de données

- **DR-194**: L’application doit utiliser une base de données stockée localement en fichiers binaires.
- **DR-195**: Les données peuvent être sérialisées en binaire dans des fichiers locaux structurés par entité ou par agrégat fonctionnel.
- **DR-196**: Le stockage binaire doit permettre la lecture/écriture transactionnelle simple sans dépendance à un serveur de base de données externe.
- **DR-197**: La structure des fichiers doit préserver l’intégrité des entités et la cohérence des relations.

## 8. Règles d’affaires

- **BR-194**: Un projet doit être identifiable de manière unique dans le contexte de l’agence.
- **BR-195**: Une tâche doit toujours appartenir à un projet.
- **BR-196**: Une user story doit toujours appartenir à un projet.
- **BR-197**: Une tâche non assignée doit être repérable comme telle.
- **BR-198**: Une tâche assignée doit référencer un utilisateur actif ou historiquement valide.
- **BR-199**: Une tâche en retard est une tâche dont la date limite est dépassée et le statut n’est pas terminé.
- **BR-200**: Une tâche terminée ne doit pas être considérée comme en retard.
- **BR-201**: Un projet archivé ne doit pas apparaître par défaut dans la liste des projets actifs.
- **BR-202**: Les tâches d’un projet archivé ne doivent plus être modifiables sauf par des utilisateurs autorisés.
- **BR-203**: Seuls les utilisateurs autorisés peuvent supprimer ou archiver un projet.
- **BR-204**: Seuls les utilisateurs autorisés peuvent modifier les rôles et permissions.
- **BR-205**: Une notification doit être générée lors de l’assignation d’une tâche.
- **BR-206**: Une notification doit être générée lorsqu’une tâche approche de sa date limite selon une règle configurable.

## 9. Contraintes du système

- **SYS-207**: L’application doit être développée comme application web.
- **SYS-208**: L’application doit centraliser la gestion de projet dans une interface unique.
- **SYS-209**: L’application doit viser une petite agence digitale tout en restant extensible.
- **SYS-210**: L’application doit réduire la dépendance aux tableurs, e-mails et réunions informelles.
- **SYS-211**: L’application doit permettre un suivi quotidien de l’avancement.
- **SYS-212**: L’application doit être modulaire pour permettre l’ajout futur d’intégrations, rapports ou exportations.

## 10. Critères d’acceptation globaux

- **AC-213**: Le chef de projet peut créer un projet, y ajouter des tâches, assigner des membres, définir des priorités et suivre l’avancement depuis le tableau de bord.
- **AC-214**: Le développeur peut consulter les tâches qui lui sont assignées, modifier leur statut et contribuer au backlog.
- **AC-215**: Le membre de l’équipe peut consulter les projets auxquels il participe et recevoir les notifications pertinentes.
- **AC-216**: L’administrateur peut gérer les utilisateurs, rôles et permissions.
- **AC-217**: Le système permet de visualiser clairement les tâches à faire, en cours, terminées, bloquées et en retard.
- **AC-218**: Le système permet d’identifier rapidement les priorités d’un projet.
- **AC-219**: Le système permet de comprendre la finalité des tâches via les user stories associées.
- **AC-220**: Le système réduit les oublis grâce à l’assignation, aux échéances et aux notifications.
- **AC-221**: Le système fournit une vue centralisée et fiable de l’état d’avancement.
- **AC-222**: Le système est suffisamment clair et structuré pour être utilisé quotidiennement sans formation complexe.

## 11. Hors périmètre initial

- **OOS-223**: Pas de messagerie instantanée complète.
- **OOS-224**: Pas de remplacement de Slack, Teams ou Discord.
- **OOS-225**: Pas de facturation client dans la première version.
- **OOS-226**: Pas de gestion avancée des budgets dans la première version.
- **OOS-227**: Pas de planification complète des ressources humaines dans la première version.
- **OOS-228**: Pas d’intégration externe obligatoire dans la première version.
- **OOS-229**: Pas d’application mobile native dans la première version.
- **OOS-230**: Pas de gestion avancée des feuilles de temps dans la première version.

## 12. Modèle de données et entités clés

### Utilisateur
- Identifiant unique
- Nom complet
- Adresse courriel
- Rôles attribués
- Statut de compte (actif, désactivé)
- Projets associés
- Notifications

### Projet
- Identifiant unique
- Nom
- Description
- Date de livraison prévue
- Statut (non démarré, en cours, en attente, terminé, archivé)
- Priorité ou catégorie
- Membres associés
- Tâches liées
- User stories liées
- Historique des modifications

### Tâche
- Identifiant unique
- Titre
- Description
- Statut
- Priorité
- Projet associé
- Responsable (utilisateur ou nul)
- Date limite
- Estimation d’effort
- Liste de dépendances
- Commentaires
- Fichiers/joints ou liens
- Historique des modifications

### User story
- Identifiant unique
- Titre
- Description structurée
- Acteur concerné
- Besoin
- Résultat attendu
- Critères d’acceptation
- Projet associé
- Statut
- Priorité
- Tâches associées
- Historique des modifications

### Notification
- Identifiant unique
- Destinataire utilisateur
- Type d’événement
- Contenu texte
- Statut lu/non lu
- Date de création

### Historique
- Entité source
- Utilisateur auteur
- Date de modification
- Type de changement
- Valeur précédente / nouvelle valeur

## 13. Notes d’implémentation

- La base de données doit être implémentée en fichiers binaires locaux, sans dépendance à un SGBD externe.
- Le stockage binaire doit permettre des opérations CRUD, des recherches indexées simples et une lecture cohérente des relations.
- Les fichiers doivent être organisés pour limiter les risques de corruption et faciliter la maintenance en test et en production.
- Le backend peut exposer des API REST ou GraphQL pour la gestion des projets, tâches, user stories, utilisateurs et notifications.
- Le frontend doit proposer une interface responsive pour ordinateur portable et bureau.

## 14. Critères de succès mesurables

- **SC-001**: Création et modification d’un projet disponibles en moins de 3 clics pour le chef de projet.
- **SC-002**: Un développeur peut voir toutes ses tâches assignées en moins de 5 secondes.
- **SC-003**: Le tableau de bord affiche les indicateurs principaux sans rechargements complets inutiles.
- **SC-004**: Les projets non associés sont inaccessibles pour les utilisateurs non autorisés.
- **SC-005**: Une tâche en retard est identifiée et signalée automatiquement.
- **SC-006**: La base de données fonctionne uniquement en fichiers binaires locaux et accepte les opérations de lecture/écriture sur les entités principales.

## 15. Hypothèses

- Les utilisateurs disposent d’un navigateur web moderne.
- La version initiale vise les postes de travail plutôt que les mobiles.
- Aucun service externe de base de données ne sera utilisé.
- La configuration HTTPS sera gérée au déploiement pour l’environnement de production.
- La priorité est la mise en place d’un outil interne simple, extensible et autonome.
