import random

class Robot:
    def __init__(self, nom, difficulte):
        self.nom = nom
        self.difficulte = difficulte
        self.pv = 100
        self.attaque = 10
        self.defense = 5
        self.niveau = 1
        self.exp = 0
        self.améliorations_disponibles = 0
        self.inventaire = []
        self.objets_equipes = {
            "arme": None,
            "armure": None,
            "implant": None
        }
        self.quêtes = []
        self.quêtes_complétées = 0
        self.reputation = 0
        self.jours = 0
        self.est_rebelle = False

        # 10% de chance de devenir un robot rebelle au début du jeu
        if random.random() < 0.1:
            self.devenir_rebelle()

    def devenir_rebelle(self):
        self.est_rebelle = True
        self.attaque += 15
        self.defense -= 5
        self.pv -= 20
        print(f"{self.nom} est devenu un robot rebelle! Attaque +15, Défense -5, PV -20.")
        print("En tant que robot rebelle, vous aidez les rebelles au lieu de les combattre.")

    def attaquer(self, ennemi, choix):
        if self.est_rebelle:
            print("En tant que robot rebelle, vous refusez de combattre les rebelles.")
            return False
        if choix == "tuer":
            dégats = max(0, self.attaque - ennemi.defense // 2)
            ennemi.pv -= dégats
            print(f"{self.nom} attaque {ennemi.nom} et inflige {dégats} dégâts!")
            if ennemi.pv <= 0:
                print(f"{ennemi.nom} est vaincu!")
                self.gagner_exp(ennemi.exp)
                if ennemi.objet:
                    self.inventaire.append(ennemi.objet)
                    print(f"Vous avez obtenu {ennemi.objet}!")
        elif choix == "infecter":
            print(f"{self.nom} infecte {ennemi.nom} avec le virus!")
            ennemi.infecte = True
            self.gagner_exp(ennemi.exp // 2)
        return True

    def gagner_exp(self, exp):
        self.exp += exp
        print(f"{self.nom} gagne {exp} points d'expérience.")
        if self.difficulte == "difficile":
            if self.exp >= self.niveau * 10:
                self.niveau += 1
                self.exp = 0
                self.attaque += 5
                self.defense += 2
                self.pv += 20
                print(f"{self.nom} monte de niveau! Niveau {self.niveau}, Attaque {self.attaque}, Défense {self.defense}, PV {self.pv}")
                if self.niveau % 5 == 0:
                    self.améliorations_disponibles += 1
                    print(f"Amélioration disponible! (Total: {self.améliorations_disponibles})")

    def utiliser_objet(self, objet):
        if objet in self.inventaire:
            if objet == "Potion de soin":
                self.pv = min(100, self.pv + 30)
                print(f"{self.nom} utilise une Potion de soin et récupère 30 PV.")
            elif objet == "Implant de Soin":
                self.pv = min(100, self.pv + 20)
                print(f"{self.nom} utilise un Implant de Soin et récupère 20 PV.")
            self.inventaire.remove(objet)

    def équiper(self, objet):
        if objet in self.inventaire:
            if "Arme" in objet:
                self.objets_equipes["arme"] = objet
                self.attaque += 10
                print(f"{self.nom} équipe {objet} et gagne +10 en attaque.")
            elif "Armure" in objet:
                self.objets_equipes["armure"] = objet
                self.defense += 10
                print(f"{self.nom} équipe {objet} et gagne +10 en défense.")
            elif "Implant" in objet:
                self.objets_equipes["implant"] = objet
                self.pv += 20
                print(f"{self.nom} équipe {objet} et gagne +20 PV.")
            self.inventaire.remove(objet)

    def améliorer(self, attribut):
        if self.améliorations_disponibles > 0:
            if attribut == "attaque":
                self.attaque += 10
                print(f"{self.nom} améliore son attaque! Attaque: {self.attaque}")
            elif attribut == "defense":
                self.defense += 10
                print(f"{self.nom} améliore sa défense! Défense: {self.defense}")
            elif attribut == "pv":
                self.pv += 20
                print(f"{self.nom} améliore ses PV! PV: {self.pv}")
            self.améliorations_disponibles -= 1
        else:
            print("Aucune amélioration disponible.")

    def afficher_stats(self):
        print(f"\n=== STATS DE {self.nom} ===")
        print(f"PV: {self.pv}")
        print(f"Attaque: {self.attaque}")
        print(f"Défense: {self.defense}")
        print(f"Niveau: {self.niveau}")
        print(f"Exp: {self.exp}/{self.niveau * 10}")
        print(f"Quêtes complétées: {self.quêtes_complétées}")
        print(f"Réputation: {self.reputation}")
        print(f"Jours: {self.jours}")
        print(f"Inventaire: {', '.join(self.inventaire) if self.inventaire else 'Vide'}")
        print(f"Arme: {self.objets_equipes['arme'] if self.objets_equipes['arme'] else 'Aucune'}")
        print(f"Armure: {self.objets_equipes['armure'] if self.objets_equipes['armure'] else 'Aucune'}")
        print(f"Implant: {self.objets_equipes['implant'] if self.objets_equipes['implant'] else 'Aucun'}")
        if self.est_rebelle:
            print("Status: Robot Rebelle - Aide les rebelles")

class Humain:
    def __init__(self, nom, pv, attaque, defense, exp, objet=None):
        self.nom = nom
        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.exp = exp
        self.infecte = False
        self.objet = objet

    def attaquer(self, robot):
        if not self.infecte:
            dégats = max(0, self.attaque - robot.defense // 2)
            robot.pv -= dégats
            print(f"{self.nom} attaque {robot.nom} et inflige {dégats} dégâts!")
        else:
            print(f"{self.nom} est infecté et ne peut pas attaquer correctement!")
            dégats = max(0, self.attaque // 2 - robot.defense // 2)
            robot.pv -= dégats
            print(f"{self.nom} attaque faiblement {robot.nom} et inflige {dégats} dégâts!")

def combat(robot, ennemi):
    print(f"\nCombat: {robot.nom} vs {ennemi.nom}")
    if robot.est_rebelle:
        print("En tant que robot rebelle, vous refusez de combattre les rebelles.")
        return False
    while robot.pv > 0 and ennemi.pv > 0:
        print(f"\n{robot.nom}: PV {robot.pv}, Attaque {robot.attaque}, Défense {robot.defense}")
        print(f"{ennemi.nom}: PV {ennemi.pv}, Attaque {ennemi.attaque}, Défense {ennemi.defense}")
        print("\nOptions de combat:")
        print("1. Attaquer (tuer)")
        print("2. Infecter")
        print("3. Utiliser un objet")
        print("4. Fuir")
        choix = input("Que faire ? ").strip()
        if choix == "1":
            robot.attaquer(ennemi, "tuer")
        elif choix == "2":
            robot.attaquer(ennemi, "infecter")
        elif choix == "3":
            print(f"Inventaire: {', '.join(robot.inventaire) if robot.inventaire else 'Vide'}")
            objet = input("Quel objet utiliser ? ").strip()
            if objet in robot.inventaire:
                robot.utiliser_objet(objet)
            else:
                print("Objet non trouvé dans l'inventaire.")
        elif choix == "4":
            print("Vous fuyez le combat!")
            return False
        else:
            print("Choix invalide. Vous attaquez normalement.")
            robot.attaquer(ennemi, "tuer")
        if ennemi.pv > 0 and not ennemi.infecte:
            ennemi.attaquer(robot)
        if robot.pv <= 0:
            print("\nVotre robot a été vaincu. GAME OVER.")
            return False
    return True

def choisir_difficulte():
    print("Choisissez la difficulté:")
    print("1. Facile")
    print("2. Moyen")
    print("3. Difficile")
    choix = input("Entrez le numéro de la difficulté: ").strip()
    if choix == "1":
        return "facile"
    elif choix == "2":
        return "moyen"
    else:
        return "difficile"

def améliorer_attributs(robot):
    if robot.difficulte == "difficile" and robot.améliorations_disponibles > 0:
        print("\nAméliorations disponibles:")
        print("1. Attaque")
        print("2. Défense")
        print("3. PV")
        choix = input("Quel attribut améliorer? ").strip()
        if choix == "1":
            robot.améliorer("attaque")
        elif choix == "2":
            robot.améliorer("defense")
        elif choix == "3":
            robot.améliorer("pv")
        else:
            print("Choix invalide.")

def main():
    print("Bienvenue dans Néo-Terra: Robot Infecté")
    nom = input("Entrez le nom de votre robot: ")
    difficulte = choisir_difficulte()
    robot = Robot(nom, difficulte)

    humains = [
        Humain("Humain Rebelle", 50, 10, 5, 10),
        Humain("Humain Résistant", 70, 15, 10, 15),
        Humain("Humain Élite", 100, 20, 15, 20),
        Humain("Chef Rebelle", 150, 25, 20, 25)
    ]

    for i, humain in enumerate(humains):
        print(f"\n=== Combat {i + 1} ===")
        if not combat(robot, humain):
            if robot.est_rebelle:
                print("\nEn tant que robot rebelle, vous avez décidé de ne pas combattre les rebelles.")
                print("Votre mission est terminée.")
                break
            else:
                print("\nVotre robot a été vaincu. GAME OVER.")
                break
        print(f"\n{robot.nom} a vaincu {humain.nom}!")
        if robot.difficulte == "difficile" and robot.niveau % 5 == 0:
            améliorer_attributs(robot)

    if robot.pv > 0 and not robot.est_rebelle:
        print("\nFélicitations! Votre robot a accompli sa mission.")
    elif robot.est_rebelle:
        print("\nEn tant que robot rebelle, vous avez aidé les rebelles et accompli votre mission.")

if __name__ == "__main__":
    main()
