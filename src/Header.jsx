export default function Header() {
  return (
    <div
      className="h-screen w-screen bg-cover bg-center bg-no-repeat relative overflow-hidden"
      style={{ backgroundImage: "url('/background_image.png')" }}
    >
      <div className="absolute top-6 left-6 text-white text-3xl font-bold leading-snug">
        <div>Welcome to</div>
        <div>AI Resume Parsing System</div>
      </div>
    </div>
  );
}
